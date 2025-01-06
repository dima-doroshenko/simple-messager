from typing import TYPE_CHECKING
import uuid

from fastapi import Response, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from database import UsersOrm, ChatsOrm, ChatType, UserChatsOrm
from utils import auth
from config import settings
from schemas import CreatePrivateChat, CreateGroupChat

from .chat import Chat

if TYPE_CHECKING:
    from .crud import Crud

class User:

    def __init__(
        self,
        crud: 'Crud',
        user_obj: UsersOrm
    ):
        self.crud = crud
        self.session = crud.session
        self.obj = user_obj
    
    def check_password(self, password: str) -> bool:
        return auth.check_password(
            password=password,
            hashed_password=self.obj.hashed_password
        )
    
    def login(
        self,
        credentials: HTTPBasicCredentials,
        response: Response
    ):
        session_id = uuid.uuid4().hex
        self.crud.set_cookie_data(session_id, credentials.model_dump())
        response.set_cookie(settings.auth.session_id_key, session_id)

    async def _create_chat(
        self, 
        type: ChatType,
        with_users: int | list[int],
        name: str = 'auto', 
        description: str | None = None
    ) -> int:
        if type == ChatType.private:
            if with_users == self.obj.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Can not create a private chat with yourself'
                )
            
        if isinstance(with_users, int):
            with_users = [with_users]
        else:
            with_users = with_users.copy()
        
        await self.crud.check_if_users_exist(with_users)

        chat = ChatsOrm(
            type=type,
            name=name,
            description=description,
            owner_id=self.obj.id
        )

        self.session.add(chat)

        chat_members = with_users if self.obj.id in with_users else (self.obj.id, *with_users)

        objects = [
            UserChatsOrm(
                user_id=user_id,
                chat_id=chat.id
            ) for user_id in chat_members
        ]
        self.session.add_all(objects)
        await self.session.flush()
        return chat.id

    async def create_private_chat(
        self, data: CreatePrivateChat
    ) -> int:
        return await self._create_chat(
            type=ChatType.private,
            with_users=data.with_user,
        )

    async def create_group_chat(
        self, data: CreateGroupChat
    ) -> int:
        return await self._create_chat(
            type=ChatType.group,
            with_users=data.with_users,
            name=data.name,
            description=data.description
        )

    async def get_chat(
        self, chat_id: int,
        check_if_owner: bool = True
    ) -> Chat | None :
        obj = await self.session.get(ChatsOrm, chat_id)

        if obj is not None:

            if check_if_owner and (obj.owner_id != self.obj.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not the owner of the chat'
                )
            return Chat(self.crud, obj)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Chat with id {chat_id} not found'
        )