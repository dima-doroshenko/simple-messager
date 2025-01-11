from typing import TYPE_CHECKING
import uuid

from fastapi import Response, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from sqlalchemy import select

from database import UsersOrm, GroupChatsOrm, UserChatsOrm, PrivateChatsOrm
from utils import auth
from config import settings
from schemas import CreatePrivateChat, CreateGroupChat

from .group_chat import GroupChat
from .private_chat import PrivateChat
from .abc import AbstractDTO

if TYPE_CHECKING:
    from .crud import Crud

class User(AbstractDTO):

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

    async def create_private_chat(
        self, data: CreatePrivateChat
    ) -> int:
        
        if data.with_user == self.obj.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Can not create a private chat with yourself'
            )
        await self.crud.check_if_users_exist(data.with_user)
        await self.check_if_private_chat_exists(data.with_user)

        chat = PrivateChatsOrm(
            user_1=self.obj.id,
            user_2=data.with_user
        )
        self.session.add(chat)
        await self.session.flush()
        
        return chat.id

    async def create_group_chat(
        self, data: CreateGroupChat
    ) -> int:
        with_users = data.with_users.copy()
        await self.crud.check_if_users_exist(with_users)

        chat = GroupChatsOrm(
            name=data.name,
            description=data.description,
            owner_id=self.obj.id
        )
        self.session.add(chat)
        await self.session.flush()

        chat_members = with_users if self.obj.id in with_users else (self.obj.id, *with_users)
        objects = [
            UserChatsOrm(
                user_id=user_id,
                chat_id=chat.id
            ) for user_id in chat_members
        ]
        self.session.add_all(objects)
        await self.session.flush(objects)

        return chat.id
    
    async def get_group_chat(
        self, chat_id: int,
        check_if_owner: bool = True,
        check_if_member: bool = True
    ) -> GroupChat | None :
        chat_id = -chat_id
        obj = await self.session.get(GroupChatsOrm, chat_id)
        
        if obj is not None:

            chat = GroupChat(obj, self)

            if check_if_member and (self.obj.id not in chat.with_users):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not a member of this chat'
                )

            if check_if_owner and (obj.owner_id != self.obj.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='You are not the owner of this chat'
                )
            return chat
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Chat with id {-chat_id} not found'
        )
    
    async def get_private_chat(
        self, other_user_id: int, raise_exc: bool = True
    ) -> PrivateChat | None:
        user_ids = (other_user_id, self.obj.id)
        query = (
            select(PrivateChatsOrm)
            .where(
                (PrivateChatsOrm.user_1.in_(user_ids)) &
                (PrivateChatsOrm.user_2.in_(user_ids))
            )
        )
        res = await self.session.execute(query) 
        obj = res.scalars().one_or_none() 

        if obj:
            return PrivateChat(obj, self)
        
        if raise_exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Chat with user id {other_user_id} not found'
            )
        
    async def check_if_private_chat_exists(
        self, user_id: int, raise_exc: bool = True
    ):
        chat = await self.get_private_chat(user_id, raise_exc=False)
        result = chat is not None

        if raise_exc and result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Chat with this user has already created'
            )
        
        return result
    
    async def get_chat_ids_list(self) -> list[int]:
        query = (
            select(PrivateChatsOrm)
            .where(
                (PrivateChatsOrm.user_1 == self.obj.id) | 
                (PrivateChatsOrm.user_2 == self.obj.id)
            )
        )
        res = await self.session.execute(query)
        result = [
            obj.user_1 if obj.user_1 != self.obj.id else obj.user_2 
            for obj in res.scalars().all()
        ]

        query = (
            select(UserChatsOrm)
            .where(UserChatsOrm.user_id == self.obj.id)
        )
        res = await self.session.execute(query)
        for obj in res.scalars().all():
            result.append(-obj.chat_id)

        return result