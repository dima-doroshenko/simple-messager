from fastapi import HTTPException, status

from pydantic import ValidationError

from .schemas import UserLogin


def validate_login(username: str, password: str):
    try:
        UserLogin(username=username, password=password)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors()
        )