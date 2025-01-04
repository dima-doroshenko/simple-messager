from datetime import datetime

from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    name: str
    username: str
    description: str | None
    created_at: datetime