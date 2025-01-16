from fastapi import APIRouter

from utils import get_current_user
from schemas import Answer, CreatePrivateChat, CreateGroupChat

router = APIRouter()

@router.post('/private')
async def create_private_chat(
    data: CreatePrivateChat,
    user: get_current_user
) -> Answer:
    await user.create_private_chat(data)
    return Answer(
        data={'chat_id': data.with_user},
        msg='Private chat created'
    )

@router.post('/group')
async def create_group_chat(
    data: CreateGroupChat,
    user: get_current_user
) -> Answer:
    chat_id = await user.create_group_chat(data)
    return Answer(
        data={'chat_id': chat_id},
        msg='Group chat created'
    )

@router.patch('/{chat_id}')
async def edit_chat(
    chat_id: int,
    user: get_current_user,
    new_name: str = None,
    new_description: str = None
) -> Answer:
    chat = await user.get_group_chat(chat_id)
    
    if new_name is not None:
        chat.obj.name = new_name
    if new_description is not None:
        if new_description == '':
            new_description = None
        chat.obj.description = new_description

    return Answer(msg='Chat edited')

@router.delete('/{chat_id}')
async def delete_chat(
    chat_id: int,
    user: get_current_user
) -> Answer:
    chat = await user.get_group_chat(chat_id)
    await chat.delete()
    return Answer(msg='Chat deleted')

@router.post('/{chat_id}/user')
async def invite_user(
    chat_id: int,
    user_id: int,
    user: get_current_user
) -> Answer:
    chat = await user.get_group_chat(chat_id)
    await chat.invite_user(user_id)
    return Answer(msg='User invited')

@router.delete('/{chat_id}/user')
async def kick_user(
    chat_id: int,
    user_id: int,
    user: get_current_user
) -> Answer:
    chat = await user.get_group_chat(chat_id)
    await chat.kick_user(user_id)
    return Answer(msg='User kicked')