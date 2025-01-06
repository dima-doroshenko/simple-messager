import json

from fastapi import Depends, HTTPException, status

from sqlalchemy import select, func

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
    ) -> User | None:
        query = (
            select(UsersOrm)
            .where(UsersOrm.username == username)
        )
        res = await self.session.execute(query)
        user_obj = res.scalars().one_or_none()

        if user_obj is not None:
            return User(self, user_obj)
        
    async def get_user_by_id(
        self, id: int
    ) -> User | None:
        obj = await self.session.get(UsersOrm, id)
        if obj is not None:
            return User(self, obj)
        
    async def check_if_users_exist(
        self, 
        user_ids: int | list[int],
        raise_exc: bool = True
    ) -> bool:
        if isinstance(user_ids, int):
            user_ids = [user_ids]
        query = (
            select(UsersOrm.id)
            .where(UsersOrm.id.in_(user_ids))
        )

        res = await self.session.execute(query)
        found_users = res.all()
        result = len(user_ids) == len(found_users)
        
        if raise_exc and not result:

            for id in user_ids:
                if id not in found_users:
                    break

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with id {id} not found'
            )
        
        return result