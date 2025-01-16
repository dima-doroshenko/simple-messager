from fastapi import APIRouter

from utils import get_current_user
from schemas import Answer, ReadUser

router = APIRouter()


@router.patch("")
async def edit_profile(
    user: get_current_user, new_name: str = None, new_description: str = None
) -> Answer:

    if new_name is not None:
        user.obj.name = new_name
    if new_description is not None:
        if new_description == "":
            new_description = None
        user.obj.description = new_description

    return Answer(msg="Profile edited")


@router.get("")
async def get_me(user: get_current_user) -> ReadUser:
    return user.obj.as_dict
