from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, BLOB

from ..db import Base
from ..annotations import created_at, updated_at, intpk, str32, optional_str256

if TYPE_CHECKING:
    from .chats import ChatsOrm


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    hashed_password: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    name: Mapped[str32]
    username: Mapped[str] = mapped_column(String(16), unique=True)
    description: Mapped[optional_str256]

    chats: Mapped[list['ChatsOrm']] = relationship(lazy='selectin', back_populates='members')
    


