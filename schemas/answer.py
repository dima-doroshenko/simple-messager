from pydantic import BaseModel, Field

class Answer(BaseModel):
    ok: bool = True
    data: dict = Field(default_factory=dict)
    msg: str = ''