from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

class Base(DeclarativeBase): ...
engine = create_async_engine(settings.db.url)
session_factory = async_sessionmaker(engine)