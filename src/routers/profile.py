from fastapi import APIRouter, Depends

from utils import get_current_user
from repository import User
from schemas import Answer, UserRead

router = APIRouter()

@router.patch('/name')
async def update_name(
    new_name: str,
    user: User = Depends(get_current_user)
) -> Answer:
    user.obj.name = new_name
    return Answer(msg='Name edited')

@router.patch('/description')
async def update_description(
    new_description: str | None = None,
    user: User = Depends(get_current_user)
) -> Answer:
    user.obj.description = new_description
    return Answer(msg='Description edited')

@router.get('/')
async def get_me(
    user: User = Depends(get_current_user)
) -> UserRead:
    return user.obj.as_dict