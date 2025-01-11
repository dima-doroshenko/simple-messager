from typing import TYPE_CHECKING

from sqlalchemy import delete

from database import PrivateChatsOrm, ChatType
from schemas import ReadPrivateChat

from .chat import Chat
from .abc import AbstractDTO

if TYPE_CHECKING:
    from .user import User


class PrivateChat(Chat, AbstractDTO):
    type: ChatType = ChatType.private

    def __init__(
        self,
        chat_obj: PrivateChatsOrm,
        user: 'User'
    ):
        self.crud = user.crud
        self.session = self.crud.session
        self.obj = chat_obj
        self.user = user
        self.with_user = self.obj.user_1 if self.obj.user_1 != self.user.obj.id else self.obj.user_2
        user_ids = (self.user.obj.id, self.with_user)
        self.whereclause = (
            (PrivateChatsOrm.user_1.in_(user_ids)) &
            (PrivateChatsOrm.user_2.in_(user_ids))
        )

    async def send_message(self, text: str):
        return await self.crud._send_message(
            self, text=text,
            chat_id=self.obj.id, from_user=self.user.obj.id
        )

    async def get_info(self) -> ReadPrivateChat:
        return ReadPrivateChat(
            with_user=(await self.crud.get_user_by_id(self.with_user)).obj.as_dict,
            messages=await self._get_messages()
        )
    
    async def leave(self) -> None:
        user_ids = (self.user.obj.id, self.with_user)
        stmt = (
            delete(PrivateChatsOrm)
            .where(
                (PrivateChatsOrm.user_1.in_(user_ids)) &
                (PrivateChatsOrm.user_2.in_(user_ids))
            )
        )
        await self.session.execute(stmt)