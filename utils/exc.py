from typing import Any
from schemas import Answer


class AnswerException(Exception):

    def __init__(self, status_code: int, msg: str, **data):
        self.status_code = status_code
        self.msg = msg
        self.data = data

    def to_dict(self) -> dict[str, Any]:
        return Answer(ok=False, data=self.data, msg=self.msg).model_dump()
