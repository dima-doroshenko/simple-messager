from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

from ..db import Base


class UserChatsOrm(Base): 
    __tablename__ = 'user_chats' 
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('group_chats.id'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'chat_id'),
    )