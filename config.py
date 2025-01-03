from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path

BASEDIR = Path(__file__).parent

class Auth(BaseModel):
    session_id_key: str = 'web-app-session-id'

class DBSettings(BaseModel):
    url: str = 'sqlite+aiosqlite:///database.db'

class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    auth: Auth = Auth()
    
settings = Settings()