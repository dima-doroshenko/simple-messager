from pydantic import BaseModel, field_validator, ValidationError, Field

allowed_symblos = 'qwertyuiopasdfghjklzxcvbnm1234567890_QWERTYUIOPASDFGHJKLZXCVBNM'

class UserLogin(BaseModel):
    username: str = Field(max_length=16, min_length=3)
    password: str = Field(min_length=8, max_length=64)

    @field_validator('username', 'password')
    def validate_username(cls, value: str):
        
        for symbol in value:
            if symbol not in allowed_symblos:
                raise ValidationError(f'Symbol {symbol!r} is not allowed')
            
        return value