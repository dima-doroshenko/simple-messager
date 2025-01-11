import asyncio

from fastapi import FastAPI

from database import Base, engine
from .routers import router

async def app_lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=app_lifespan)
app.include_router(router)