from fastapi import Cookie, Depends, Response

from repository import Crud

from .schemas import UserLogin
from .exc import (
    UnauthedException, UserNotFoundException, 
    InvalidCookieException, InvalidUsernameOrPasswordException
)

from config import settings

async def get_current_user(
    session_id: str = Cookie(alias=settings.auth.session_id_key, default=None),
    crud: Crud = Depends(Crud)
):
    if session_id is None:
        raise UnauthedException
    
    session_data = await crud.get_cookie_data(session_id)

    if session_data is None:
        raise InvalidCookieException

    credentials = UserLogin(**session_data)
    
    if not (user := await crud.get_user_by_username(credentials.username)):
        raise UserNotFoundException
    
    if not user.check_password(credentials.password):
        raise InvalidUsernameOrPasswordException
        
    return user