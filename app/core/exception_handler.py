from fastapi import FastAPI, Request
from pydantic import ValidationError
from structlog import get_logger

from app.core.errors import (
    AppError,
    ConflictAppError,
    InvalidIdentityAppError,
    NotFoundAppError,
    RateLimitedAppError,
    UnauthorizedAppError,
    ValidationAppError,
)
from app.core.response import error

logger = get_logger(__name__)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        status_code = 400
        if isinstance(exc, NotFoundAppError):
            status_code = 404
        elif isinstance(exc, ConflictAppError):
            status_code = 409
        elif isinstance(exc, InvalidIdentityAppError):
            status_code = 400
        elif isinstance(exc, RateLimitedAppError):
            status_code = 429
        elif isinstance(exc, UnauthorizedAppError):
            status_code = 401
        elif isinstance(exc, ValidationAppError):
            status_code = 422

        return error(
            exc.code,
            exc.message,
            field_errors=exc.field_errors,
            status_code=status_code,
        )

    @app.exception_handler(ValidationError)
    async def handle_pydantic_validation_error(request: Request, exc: ValidationError):
        return error(
            "validation_error",
            "Validation failed",
            field_errors={str(err["loc"]): err["msg"] for err in exc.errors()},
            status_code=422,
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        logger.exception("unhandled_exception", exc_info=exc)
        return error(
            "internal_error",
            "An unexpected error occurred.",
            status_code=500,
        )
