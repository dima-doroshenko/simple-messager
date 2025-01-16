from fastapi import APIRouter

from utils import get_current_user, get_current_chat
from schemas import Answer, ReadPrivateChat, ReadGroupChat

router = APIRouter()


@router.get("")
async def get_chat_ids_list(user: get_current_user) -> list[int]:
    return await user.get_chat_ids_list()


@router.get("/{chat_id}")
async def get_chat(
    chat: get_current_chat, messages_page: int = 1
) -> ReadPrivateChat | ReadGroupChat:
    return await chat.get_info(messages_page)


@router.delete("/{chat_id}")
async def leave_chat(chat: get_current_chat) -> Answer:
    await chat.leave()
    return Answer(msg="Chat left")
