import asyncio

from fastapi import FastAPI

from database import Base, engine


app = FastAPI()

async def init_db():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run_coroutine_threadsafe(
    init_db(), asyncio.get_running_loop()
)