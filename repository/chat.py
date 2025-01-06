from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy.exc import IntegrityError

from database import ChatsOrm, ChatType, UserChatsOrm

if TYPE_CHECKING:
    from .crud import Crud


class Chat:

    def __init__(
        self,
        crud: 'Crud',
        chat_obj: ChatsOrm
    ):
        self.crud = crud
        self.session = crud.session
        self.obj = chat_obj

    @property
    def is_private(self) -> bool:
        return self.obj.type == ChatType.private
    
    async def invite_user_to_chat(self, user_id: int) -> None:
        await self.crud.check_if_users_exist(user_id)
        try:
            obj = UserChatsOrm(
                chat_id=self.obj.id,
                user_id=user_id
            )
            self.session.add(obj)
            await self.session.flush()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with id {user_id} has already joined the chat'
            )
