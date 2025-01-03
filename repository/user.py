from typing import TYPE_CHECKING
import uuid

from fastapi import Response
from fastapi.security import HTTPBasicCredentials

from database import UsersOrm
from utils import auth
from config import settings

if TYPE_CHECKING:
    from .crud import Crud

class User:

    def __init__(
        self,
        crud: 'Crud',
        user_obj: UsersOrm
    ):
        self.crud = crud
        self.session = crud.session
        self.obj = user_obj
    
    def check_password(self, password: str) -> bool:
        return auth.check_password(
            password=password,
            hashed_password=self.obj.hashed_password
        )
    
    def login(
        self,
        credentials: HTTPBasicCredentials,
        response: Response
    ):
        session_id = uuid.uuid4().hex
        self.crud.set_cookie_data(session_id, credentials.model_dump())
        response.set_cookie(settings.auth.session_id_key, session_id)