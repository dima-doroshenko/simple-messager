from fastapi import APIRouter

from utils import get_current_chat, get_current_message
from schemas import Answer, Message

router = APIRouter()


@router.post("")
async def send_message(text: str, chat: get_current_chat) -> Message:
    return await chat.send_message(text)


@router.delete("")
async def delete_message(msg: get_current_message) -> Answer:
    await msg.delete()
    return Answer(msg="Message deleted")


@router.patch("")
async def edit_message(new_text: str, msg: get_current_message) -> Answer:
    await msg.edit(new_text)
    return Answer(msg="Message edited")
