from typing import TYPE_CHECKING, Union

from database import ChatType, PrivateChatsOrm, GroupChatsOrm, Base

if TYPE_CHECKING:
    from ..user import User


class AbstractChat:
    type: ChatType
    user: 'User'
    obj: Union[PrivateChatsOrm, GroupChatsOrm]

    def __init__(
        self,
        chat_obj: Base,
        user: 'User'
    ):
        raise NotImplementedError

    async def leave(self) -> None:
        raise NotImplementedError

    async def delete(self) -> None:
        raise NotImplementedError

    async def get_info(self):
        raise NotImplementedError

    async def send_message(self, text: str) -> None:
        raise NotImplementedError