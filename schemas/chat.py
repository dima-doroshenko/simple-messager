from datetime import datetime

from pydantic import BaseModel

from .message import Message
from .user import ReadUser

class CreatePrivateChat(BaseModel):
    with_user: int

class CreateGroupChat(BaseModel):
    name: str
    description: str | None = None
    with_users: list[int]

class ReadPrivateChat(BaseModel):
    with_user: ReadUser
    messages: list[Message]

class ReadGroupChat(CreateGroupChat):
    owner_id: int
    with_users: list[ReadUser]
    messages: list[Message]