import json

from fastapi import Depends, status

from sqlalchemy import select

from database import (
    AsyncSession,
    session_dependency,
    CookiesOrm,
    UsersOrm,
    ChatType,
    MessagesOrm,
)
from repository import abc
from utils.auth import hash_password
from utils.exc import AnswerException
from cache import AsyncLRU
from schemas import Message
from config import settings

from repository.user import User

UserNotFoundException = lambda user_id: AnswerException(
    status_code=status.HTTP_404_NOT_FOUND, msg=f"User with id {user_id} not found"
)


class Crud:

    def __init__(self, session: AsyncSession = Depends(session_dependency)):
        self.session = session

    def set_cookie_data(self, session_id: str, data: dict):
        self.session.add(CookiesOrm(key=session_id, value=json.dumps(data)))

    @AsyncLRU(maxsize=settings.cache.cookie_cache_maxsize)
    async def get_cookie_data(self, session_id: str) -> dict | None:
        obj = await self.session.get(CookiesOrm, session_id)
        return None if obj is None else json.loads(obj.value)

    @property
    def __dict__(self) -> dict:
        # неоходимо для кэширования через AsyncLRU
        return {}

    async def create_user(self, username: str, password: str) -> User:
        obj = UsersOrm(
            name="default", username=username, hashed_password=hash_password(password)
        )
        self.session.add(obj)
        await self.session.flush()
        return User(self, obj)

    async def get_user_by_username(self, username: str) -> User | None:
        query = select(UsersOrm).where(UsersOrm.username == username)
        res = await self.session.execute(query)
        user_obj = res.scalars().one_or_none()

        if user_obj is not None:
            return User(self, user_obj)

    async def get_user_by_id(self, user_id: int, raise_exc: bool = True) -> User | None:
        obj = await self.session.get(UsersOrm, user_id)
        if obj is not None:
            return User(self, obj)

        if raise_exc:
            raise UserNotFoundException(user_id)

    async def get_users_by_id(
        self, user_ids: int, raise_exc: bool = True
    ) -> list[User | None]:
        return [
            await self.get_user_by_id(user_id, raise_exc=raise_exc)
            for user_id in user_ids
        ]

    async def check_if_users_exist(
        self, user_ids: int | list[int], raise_exc: bool = True
    ) -> bool:
        if isinstance(user_ids, int):
            user_ids = [user_ids]
        query = select(UsersOrm.id).where(UsersOrm.id.in_(user_ids))

        res = await self.session.execute(query)
        found_users = res.all()
        result = len(user_ids) == len(found_users)

        if raise_exc and not result:

            for id in user_ids:
                if id not in found_users:
                    break

            raise UserNotFoundException(id)

        return result

    async def _send_message(
        self,
        chat: abc.AbstractChat,
        text: str,
        chat_id: int,
        from_user: int,
    ) -> Message:
        msg = MessagesOrm(
            text=text, chat_type=chat.type, chat_id=chat_id, from_user_id=from_user
        )
        self.session.add(msg)
        await self.session.flush()

        msg_dict = msg.as_dict
        if chat.type == ChatType.group:
            msg_dict["chat_id"] = -msg_dict["chat_id"]
        elif chat.type == ChatType.private:
            msg_dict["chat_id"] = chat.with_user

        return Message(**msg_dict)
