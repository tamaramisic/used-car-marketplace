from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


class CommentException(Exception):
    """Base exception for all exceptions in the comment service"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An unexpected error occurred"


class CommentNotFound(CommentException):
    """Comment not found in the database"""

    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self):
        self.detail = "Comment doesn't exist"
        super().__init__(self.detail)


class NotCommentAuthor(CommentException):
    """Anauthorized action on the comment"""

    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, action: str = "modify"):
        self.detail = f"Only the author can {action} a comment"
        super().__init__(self.detail)


class NotCommentAuthorUpdate(NotCommentAuthor):
    """Anauthorized comment updating"""

    def __init__(self):
        super().__init__(action="update")


class NotCommentAuthorDelete(NotCommentAuthor):
    """Anauthorized comment deletion"""

    def __init__(self):
        super().__init__(action="delete")


def comment_exception_handler(request: Request, exc: CommentException):
    return JSONResponse(
        status_code=getattr(exc, "status_code", 400),
        content={"detail": getattr(exc, "detail", str(exc))},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(CommentException, comment_exception_handler)
