from typing import Any, Dict, Optional

from fastapi.responses import JSONResponse


def ok(data: Any, meta: Optional[Dict[str, Any]] = None) -> JSONResponse:
    """
    Returns a standard success response.
    """
    content = {"success": True, "data": data}
    if meta:
        content["meta"] = meta
    return JSONResponse(content=content)


def paginated(data: Any, page: int, size: int, total: int) -> JSONResponse:
    """
    Returns a paginated success response.
    """
    meta = {"page": page, "size": size, "total": total}
    return ok(data, meta)


def error(
    code: str,
    title: str,
    detail: Optional[str] = None,
    field_errors: Optional[Dict[str, Any]] = None,
    status_code: int = 400,
) -> JSONResponse:
    """
    Returns a standard error response.
    """
    error_data: Dict[str, Any] = {"code": code, "title": title}
    if detail:
        error_data["detail"] = detail
    if field_errors:
        error_data["field_errors"] = field_errors

    content = {"success": False, "error": error_data}
    return JSONResponse(content=content, status_code=status_code)
