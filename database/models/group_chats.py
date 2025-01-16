from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey

from ..db import Base
from ..annotations import intpk, optional_str256, str32

if TYPE_CHECKING:
    from .user_chats import UserChatsOrm


class GroupChatsOrm(Base):
    __tablename__ = "group_chats"

    id: Mapped[intpk]

    name: Mapped[str32]
    description: Mapped[optional_str256]

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users: Mapped[list["UserChatsOrm"]] = relationship(
        "UserChatsOrm", backref="chat", lazy="selectin"
    )
