from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class CookiesOrm(Base):
    __tablename__ = 'cookies'

    key: Mapped[str] = mapped_column(unique=True, primary_key=True)
    value: Mapped[str]