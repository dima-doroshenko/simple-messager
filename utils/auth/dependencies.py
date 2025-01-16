from typing import Annotated

from fastapi import Cookie, Depends

from repository import Crud, User, Message, abc

from .schemas import UserLogin
from .exc import (
    UnauthedException,
    UserNotFoundException,
    InvalidCookieException,
    InvalidUsernameOrPasswordException,
)

from config import settings


async def _get_current_user(
    session_id: str = Cookie(alias=settings.auth.session_id_key, default=None),
    crud: Crud = Depends(Crud),
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


async def __get_chat(chat_id: int, user: User, check_if_owner: bool):
    if chat_id < 0:
        return await user.get_group_chat(chat_id, check_if_owner=check_if_owner)
    return await user.get_private_chat(chat_id)


async def _get_current_chat_check_owner(
    chat_id: int, user: User = Depends(_get_current_user)
):
    return await __get_chat(chat_id, user, check_if_owner=True)


async def _get_current_chat(chat_id: int, user: User = Depends(_get_current_user)):
    return await __get_chat(chat_id, user, check_if_owner=False)


get_current_chat = Annotated[abc.AbstractChat, Depends(_get_current_chat)]
get_current_chat_check_owner = Annotated[
    abc.AbstractChat, Depends(_get_current_chat_check_owner)
]
get_current_user = Annotated[User, Depends(_get_current_user)]


async def _get_current_message(message_id: int, chat: get_current_chat):
    return await chat.get_message(message_id)


get_current_message = Annotated[Message, Depends(_get_current_message)]
