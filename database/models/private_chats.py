from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from ..db import Base
from ..annotations import intpk

User = Annotated[
    Mapped[int], 
    mapped_column(ForeignKey("users.id", ondelete="cascade"))
]


class PrivateChatsOrm(Base):
    __tablename__ = "private_chats"

    id: Mapped[intpk]
    user_1: Mapped[User]
    user_2: Mapped[User]
