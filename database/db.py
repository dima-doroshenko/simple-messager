from typing import Any

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

class Base(DeclarativeBase):
    
    @property
    def as_dict(self) -> dict[str, Any]: 
        return {
            c.name: getattr(self, c.name) 
            for c in self.__table__.columns
        }
    
engine = create_async_engine(settings.db.url)
session_factory = async_sessionmaker(engine)

async def session_dependency():
    async with session_factory() as session:
        yield session
        await session.commit()