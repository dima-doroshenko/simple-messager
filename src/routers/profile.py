from fastapi import APIRouter, Depends

from utils import get_current_user
from repository import User
from schemas import Answer, ReadUser

router = APIRouter()

@router.patch('/')
async def edit_profile(
    new_name: str = None,
    new_description: str = None,
    user: User = Depends(get_current_user)
) -> Answer:

    if new_name is not None:
        user.obj.name = new_name
    if new_description is not None:
        if new_description == '':
            new_description = None
        user.obj.description = new_description

    return Answer(msg='Profile edited')

@router.get('/')
async def get_me(
    user: User = Depends(get_current_user)
) -> ReadUser:
    return user.obj.as_dict