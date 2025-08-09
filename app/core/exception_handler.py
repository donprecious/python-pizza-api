from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from structlog import get_logger

from app.core.exceptions import (
    AppError,
    ConflictAppError,
    InvalidIdentityAppError,
    NotFoundAppError,
    RateLimitedAppError,
    UnauthorizedAppError,
    ValidationAppError,
)
from app.core.response import ErrorResponse, error

logger = get_logger(__name__)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        status_code = 400
        error_type = "app_error"
        if isinstance(exc, NotFoundAppError):
            status_code = 404
            error_type = "not_found_error"
        elif isinstance(exc, ConflictAppError):
            status_code = 409
            error_type = "conflict_error"
        elif isinstance(exc, InvalidIdentityAppError):
            status_code = 400
            error_type = "invalid_identity_error"
        elif isinstance(exc, RateLimitedAppError):
            status_code = 429
            error_type = "rate_limited_error"
        elif isinstance(exc, UnauthorizedAppError):
            status_code = 401
            error_type = "unauthorized_error"
        elif isinstance(exc, ValidationAppError):
            status_code = 422
            error_type = "validation_error"

        response = error(
            error= ErrorResponse(
            type= error_type,
            details={"error_message": str(exc)},
            ),
            message=exc.message,
        )
        return JSONResponse(content=response.model_dump(), status_code=status_code)

    @app.exception_handler(RequestValidationError)
    async def handle_fastapi_validation_error(
        request: Request, exc: RequestValidationError
    ):
        errors = {}
        for err in exc.errors():
            field = err["loc"][-1]
            errors[field] = err["msg"]
        
        response = error(
            ErrorResponse(
            type= "request_validation_error",
            details={"detailed_error": errors},
            ),
            message="Validation failed",
        )
        return JSONResponse(content=response.model_dump(), status_code=400)

    @app.exception_handler(ResponseValidationError)
    async def handle_response_validation_error(
        request: Request, exc: ResponseValidationError
    ):
        logger.error("response_validation_error", exc_info=exc)
        response = error(
            ErrorResponse(
            type= "response_validation_error",
            details={"errors": exc.errors()},
            ),
            message="Failed to serialize response data.",
        )
        return JSONResponse(content=response.model_dump(), status_code=500)

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        logger.exception("unhandled_exception", exc_info=exc)
        
        response = error(
              ErrorResponse(
            type= "internal_server_error",
            details={"error_message": str(exc)},
            ),
            message=f"An unexpected error occurred:",
            
        )
        return JSONResponse(content=response.model_dump(), status_code=500)
