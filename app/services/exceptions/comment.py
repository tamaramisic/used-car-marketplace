from fastapi import status
from .base import AppException


class CommentException(AppException):
    """Base exception for all exceptions in the comment service"""


class CommentNotFound(CommentException):
    """Comment not found in the database"""

    status_code = status.HTTP_404_NOT_FOUND
    detail = "Comment doesn't exist"


class NotCommentAuthor(CommentException):
    """Anauthorized action on the comment"""

    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, action: str = "modify"):
        self.detail = f"Only the author can {action} a comment"
        super().__init__(detail=self.detail)


class NotCommentAuthorUpdate(NotCommentAuthor):
    """Anauthorized comment updating"""

    def __init__(self):
        super().__init__(action="update")


class NotCommentAuthorDelete(NotCommentAuthor):
    """Anauthorized comment deletion"""

    def __init__(self):
        super().__init__(action="delete")
