import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from database import Base, engine
from .routers import router
from utils import AnswerException


async def app_lifespan(_: FastAPI):
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=app_lifespan)
app.include_router(router)


@app.exception_handler(AnswerException)
async def answer_exc_handler(request: Request, exc: AnswerException):
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
