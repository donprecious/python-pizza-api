from typing import Any, Dict, Generic, Optional, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")

class ErrorResponse(BaseModel):
    type: str
    details: Optional[Dict[str, Any]] = None

class Response(BaseModel, Generic[T]):
    is_success: bool = Field(True)
    data: Optional[T] = None
    message: str = "Success"
    error: Optional[ErrorResponse] = None
    meta: Optional[Dict[str, Any]] = None


def ok(data: Any, message: str = "Success") -> Response:
    """
    Returns a standard success response.
    """
    return Response(is_success=True, data=data, message=message)


def paginated(
    data: Any, page: int, size: int, total: int, message: str = "Success"
) -> Response:
    """
    Returns a paginated success response.
    """
    return Response(
        is_success=True,
        data=data,
        message=message,
        meta={"page": page, "size": size, "total": total},
    )


def error(error: ErrorResponse, message: str = "Error") -> Response:
    """
    Returns a standard error response.
    """
    return Response(is_success=False, error=error, message=message)
