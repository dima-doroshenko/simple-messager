from datetime import datetime

from pydantic import BaseModel, Field

from database import ChatType


class Message(BaseModel):
    id: int
    text: str = Field(max_length=4096)
    created_at: datetime
    updated_at: datetime | None
    chat_type: ChatType
    chat_id: int
    from_user_id: int