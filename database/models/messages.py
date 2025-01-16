from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from ..db import Base
from ..annotations import created_at, intpk, datetoday, updated_at
from ..enums import ChatType


class MessagesOrm(Base):
    __tablename__ = 'messages'

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(String(4096))

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    date: Mapped[datetoday]
    chat_type: Mapped[ChatType]

    chat_id: Mapped[int]
    from_user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='cascade'))