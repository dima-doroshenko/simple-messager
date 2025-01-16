from typing import TYPE_CHECKING

from fastapi import status

from sqlalchemy.exc import IntegrityError
from sqlalchemy import delete

from database import GroupChatsOrm, UserChatsOrm, ChatType
from schemas import Message, ReadGroupChat
from utils.exc import AnswerException

from .chat import Chat

if TYPE_CHECKING:
    from .user import User


class GroupChat(Chat):
    type: ChatType = ChatType.group

    def __init__(self, chat_obj: GroupChatsOrm, user: "User" = None):
        self.crud = user.crud
        self.session = self.crud.session
        self.obj = chat_obj
        self.user = user
        self.with_users: tuple[int] = tuple(user.user_id for user in self.obj.users)

    async def invite_user(self, user_id: int) -> None:
        await self.crud.check_if_users_exist(user_id)
        try:
            obj = UserChatsOrm(chat_id=self.obj.id, user_id=user_id)
            self.session.add(obj)
            await self.session.flush()
        except IntegrityError:
            raise AnswerException(
                status_code=status.HTTP_409_CONFLICT,
                msg=f"User with id {user_id} has already joined the chat",
            )

    async def kick_user(self, user_id: int) -> None:
        stmt = delete(UserChatsOrm).where(
            (UserChatsOrm.chat_id == self.obj.id) & (UserChatsOrm.user_id == user_id)
        )
        await self.session.execute(stmt)

    async def send_message(self, text: str) -> Message:
        return await self.crud._send_message(
            self, text=text, chat_id=self.obj.id, from_user=self.user.obj.id
        )

    async def get_info(self, messages_page: int = 1) -> ReadGroupChat:
        return ReadGroupChat(
            name=self.obj.name,
            description=self.obj.description,
            with_users=[
                user.obj.as_dict
                for user in await self.crud.get_users_by_id(self.with_users)
            ],
            owner_id=self.obj.owner_id,
            messages=await self._get_messages(messages_page),
        )

    async def leave(self) -> None:
        if self.obj.owner_id == self.user.obj.id:
            raise AnswerException(
                status_code=status.HTTP_403_FORBIDDEN,
                msg="The owner cannot leave the chat",
            )
        
        await self.kick_user(self.user.obj.id)

    async def delete(self) -> None:
        stmt = delete(UserChatsOrm).where(UserChatsOrm.chat_id == self.obj.id)
        await self.session.execute(stmt)
        await super().delete()
