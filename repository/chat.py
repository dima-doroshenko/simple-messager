from typing import Sequence

from fastapi import status
from sqlalchemy import select, delete

from database import MessagesOrm, ChatType
from schemas import Message as MessageSchema
from utils.exc import AnswerException

from .message import Message
from .abc import AbstractChat, AbstractDTO


class Chat(AbstractChat, AbstractDTO):

    async def delete(self):
        stmt = delete(MessagesOrm).where(
            (MessagesOrm.chat_id == self.obj.id) & (MessagesOrm.chat_type == self.type)
        )
        await self.session.execute(stmt)
        await self.session.delete(self.obj)

    async def get_message(
        self, message_id: int, raise_exc: bool = True
    ) -> Message | None:
        obj = await self.session.get(MessagesOrm, message_id)

        if raise_exc and (obj is None):

            raise AnswerException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg=f"Message with id {message_id} not found",
            )

        return Message(self, obj)

    async def _get_messages(self, page: int = 1) -> Sequence[MessageSchema]:
        query = (
            select(MessagesOrm)
            .where(
                (MessagesOrm.chat_id == self.obj.id)
                & (MessagesOrm.chat_type == self.type)
            )
            .limit(100)
            .offset((page - 1) * 100)
        )

        chat_id = self.with_user if self.type == ChatType.private else None

        res = await self.session.execute(query)
        result = []

        for msg in res.scalars().all():
            msg_dict = msg.as_dict
            msg_dict["chat_id"] = chat_id if chat_id is not None else -msg.chat_id
            result.append(MessageSchema(**msg_dict))

        return result
