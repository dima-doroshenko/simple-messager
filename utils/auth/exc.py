from fastapi import status

from utils.exc import AnswerException

InvalidUsernameOrPasswordException = AnswerException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    msg='Invalid username or password'
)
UserNotFoundException = AnswerException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    msg='User not found'
)
UserWithSameUsernameAlreadyExists = AnswerException(
    status.HTTP_409_CONFLICT,
    msg='User with same username already exists'
)
UnauthedException = AnswerException(
    status_code=status.HTTP_403_FORBIDDEN,
    msg='Please, login to your account'
)
InvalidCookieException = AnswerException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    msg='Cookie is invalid'
)