from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, ForeignKey

from ..db import Base
from ..annotations import created_at, intpk

if TYPE_CHECKING:
    from .users import UsersOrm
    from .chats import ChatsOrm


class MessagesOrm(Base):
    __tablename__ = 'messages'

    id: Mapped[intpk]
    text: Mapped[str] = mapped_column(String(4096))

    created_at: Mapped[created_at]

    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id'))
    from_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    from_user: Mapped['UsersOrm'] = relationship(lazy='joined')
    chat: Mapped['ChatsOrm'] = relationship(lazy='joined', back_populates='messages')
    
