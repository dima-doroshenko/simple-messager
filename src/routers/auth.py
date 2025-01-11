from fastapi import APIRouter, Response, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from schemas import Answer
from utils.auth import validate_login, InvalidUsernameOrPasswordException, get_current_user
from repository import Crud
from config import settings

router = APIRouter()
security = HTTPBasic()

@router.post('/login/')
async def login(
    response: Response,
    credentials: HTTPBasicCredentials = Depends(security),
    crud: Crud = Depends(Crud)
) -> Answer:
    validate_login(
        username=credentials.username,
        password=credentials.password
    )

    if (user := await crud.get_user_by_username(credentials.username)):

        if user.check_password(credentials.password):

            user.login(credentials, response)
            return Answer(
                data={'user_id': user.obj.id},
                msg='Successful login'
            )

        raise InvalidUsernameOrPasswordException
    
    user = await crud.create_user(
        username=credentials.username,
        password=credentials.password
    )
    user.login(credentials, response)

    return Answer(
        data={'user_id': user.obj.id},
        msg='Successful registration'
    )

@router.post('/logout/')
async def logout(
    response: Response,
    user: get_current_user
) -> Answer:
    response.delete_cookie(settings.auth.session_id_key)
    return Answer(
        data={'user_id': user.obj.id},
        msg='Successful logout'
    )