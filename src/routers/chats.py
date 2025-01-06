from fastapi import APIRouter, Depends, HTTPException, status

from repository import User
from utils import get_current_user
from schemas import Answer, CreatePrivateChat, CreateGroupChat, InviteUser

router = APIRouter()

@router.post('/private/')
async def create_private_chat(
    data: CreatePrivateChat,
    user: User = Depends(get_current_user)
) -> Answer:
    chat_id = await user.create_private_chat(data)
    return Answer(
        data={'chat_id': chat_id},
        msg='Private chat created'
    )

@router.post('/group')
async def create_goup_chat(
    data: CreateGroupChat,
    user: User = Depends(get_current_user)
) -> Answer:
    chat_id = await user.create_group_chat(data)
    return Answer(
        data={'chat_id': chat_id},
        msg='Group chat created'
    )

@router.patch('/{chat_id}')
async def edit_chat(
    chat_id: int,
    new_name: str = None,
    new_description: str = None,
    user: User = Depends(get_current_user)
) -> Answer:
    chat = await user.get_chat(chat_id)

    if chat.is_private:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Private chat cannot be edited'
        )
    
    if new_name is not None:
        chat.obj.name = new_name
    if new_description is not None:
        if new_description == '':
            new_description = None
        chat.obj.description = new_description

    return Answer(msg='Chat edited')

@router.post('/invite_user')
async def invite_user(
    data: InviteUser,
    user: User = Depends(get_current_user)
):
    chat = await user.get_chat(data.chat_id)
    await chat.invite_user_to_chat(data.user_id)
    return Answer(msg='User invited')

@router.get('/{chat_id}')
async def get_chat(
    chat_id: int,
    user: User = Depends(get_current_user)
):
    chat = await user.get_chat(chat_id)
    return chat.obj.as_dict