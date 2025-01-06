from datetime import datetime

from pydantic import BaseModel

class ReadUser(BaseModel):
    id: int
    name: str
    username: str
    description: str | None
    created_at: datetime

class InviteUser(BaseModel):
    user_id: int
    chat_id: int