from fastapi import HTTPException, status

InvalidUsernameOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid username or password'
)
UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='User not found'
)
UserWithSameUsernameAlreadyExists = HTTPException(
    status.HTTP_409_CONFLICT,
    'User with same username already exists'
)
UnauthedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Please, login to your account'
)
InvalidCookieException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Cookie is invalid'
)