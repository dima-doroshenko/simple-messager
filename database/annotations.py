import datetime
from typing import Annotated

from sqlalchemy.orm import mapped_column
from sqlalchemy import String

now = lambda: datetime.datetime.now(datetime.timezone.utc)

created_at = Annotated[datetime.datetime, mapped_column(default=now)]
updated_at = Annotated[datetime.datetime, mapped_column(default=now, onupdate=now)]
intpk = Annotated[int, mapped_column(primary_key=True)]
optional_str256 = Annotated[str | None, mapped_column(String(256))]
str32 = Annotated[str, mapped_column(String(32))]