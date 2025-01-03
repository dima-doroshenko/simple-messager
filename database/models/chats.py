from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from ..db import Base
from ..annotations import intpk, optional_str256, str32
from ..enums import ChatType

if TYPE_CHECKING:
    from .users import UsersOrm
    from .messages import MessagesOrm


class ChatsOrm(Base):
    __tablename__ = 'chats'

    id: Mapped[intpk]
    type: Mapped[ChatType]

    name: Mapped[str32]
    description: Mapped[optional_str256]

    owner: Mapped['UsersOrm'] = relationship(lazy='joined')
    members: Mapped[list['UsersOrm']] = relationship(lazy='selectin')
    messages: Mapped[list['MessagesOrm']] = relationship(lazy='selectin')