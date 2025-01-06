from pydantic import BaseModel

class CreatePrivateChat(BaseModel):
    with_user: int

class CreateGroupChat(BaseModel):
    name: str
    description: str | None = None
    with_users: list[int]