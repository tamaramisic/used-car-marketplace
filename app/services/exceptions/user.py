from fastapi import status
from .base import AppException


class UserException(AppException):
    """Base exception for all exceptions raised for the user"""


class UserNotFound(UserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User doesn't exist"
