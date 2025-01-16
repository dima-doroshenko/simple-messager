from typing import TYPE_CHECKING, TypeAlias, Union
from pydantic import BaseModel

from database import ChatType, PrivateChatsOrm, GroupChatsOrm
from schemas import Message, ReadGroupChat, ReadPrivateChat

if TYPE_CHECKING:
    from ..user import User

ChatObject: TypeAlias = Union[PrivateChatsOrm, GroupChatsOrm]
ReadChat: TypeAlias = Union[ReadGroupChat, ReadPrivateChat]

class AbstractChat:
    type: ChatType
    user: 'User'
    obj: ChatObject

    def __init__(
        self,
        chat_obj: ChatObject,
        user: 'User'
    ):
        raise NotImplementedError

    async def leave(self) -> None:
        raise NotImplementedError

    async def delete(self) -> None:
        raise NotImplementedError

    async def get_info(self, messages_page: int = 1) -> ReadChat:
        raise NotImplementedError

    async def send_message(self, text: str) -> Message:
        raise NotImplementedError