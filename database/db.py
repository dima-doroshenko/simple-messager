from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

class Base(DeclarativeBase): ...
engine = create_async_engine(settings.db.url)
session_factory = async_sessionmaker(engine)

async def session_dependency():
    async with session_factory() as session:
        yield session
        await session.commit()