from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from ..db import Base
from ..annotations import created_at, updated_at, intpk, str32, optional_str256


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    hashed_password: Mapped[bytes]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    name: Mapped[str32]
    username: Mapped[str] = mapped_column(String(16), unique=True)
    description: Mapped[optional_str256]
