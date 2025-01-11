from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlalchemy import delete, update

from database import MessagesOrm

from .abc import AbstractDTO

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User

class Message(AbstractDTO):

    def __init__(
        self,
        chat: 'Chat',
        message_obj: MessagesOrm
    ):
        self.crud = chat.crud
        self.session = self.crud.session
        self.chat = chat
        self.user: 'User' = chat.user
        self.obj = message_obj
        self.whereclause = (
            (MessagesOrm.chat_id == self.chat.obj.id) &
            (MessagesOrm.chat_type == self.chat.type) &
            (MessagesOrm.id == self.obj.id)
        )

        if self.user.obj.id != self.obj.from_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You are not the author of this message'
            )

    async def delete(self) -> None:
        stmt = (
            delete(MessagesOrm)
            .where(self.whereclause)
        )
        await self.session.execute(stmt)

    async def edit(self, new_text: str) -> None:
        stmt = (
            update(MessagesOrm)
            .where(self.whereclause)
            .values(text=new_text)
        )
        await self.session.execute(stmt)
