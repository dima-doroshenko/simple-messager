import json

from fastapi import Depends

from sqlalchemy import select

from database import AsyncSession, session_dependency, CookiesOrm, UsersOrm
from utils.auth import hash_password

from .user import User


class Crud:

    def __init__(
        self,
        session: AsyncSession = Depends(session_dependency)
    ):
        self.session = session

    def set_cookie_data(
        self,
        session_id: str,
        data: dict
    ):
        self.session.add(
            CookiesOrm(
                key=session_id,
                value=json.dumps(data)
            )
        )

    async def get_cookie_data(
        self,
        session_id: str
    ) -> dict | None:
        obj = await self.session.get(
            CookiesOrm, session_id
        )
        return None if obj is None else json.loads(obj.value)
    
    async def create_user(
        self,
        username: str,
        password: str
    ) -> User:
        obj = UsersOrm(
            name='default',
            username=username,
            hashed_password=hash_password(password)
        )
        self.session.add(obj)
        await self.session.flush()
        return User(self, obj)
    
    async def get_user_by_username(
        self, username: str
    ):
        query = (
            select(UsersOrm)
            .where(UsersOrm.username == username)
        )
        res = await self.session.execute(query)
        user_obj = res.scalars().one_or_none()

        if user_obj is not None:
            return User(self, user_obj)