from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppException(Exception):
    """The root exception for the entire application"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "An internal server error occurred"

    def __init__(self, status_code: int = None, detail: str = None):
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail
        super().__init__(self.detail)


def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={"detail": getattr(exc, "detail", "Internal server error")},
    )


def add_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
