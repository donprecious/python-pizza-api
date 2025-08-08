from typing import Any, Dict, Optional


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        field_errors: Optional[Dict[str, Any]] = None,
    ):
        self.code = code
        self.message = message
        self.field_errors = field_errors


class ValidationAppError(AppError):
    def __init__(self, message: str, field_errors: Optional[Dict[str, Any]] = None):
        super().__init__("validation_error", message, field_errors)


class NotFoundAppError(AppError):
    def __init__(self, message: str):
        super().__init__("not_found", message)


class ConflictAppError(AppError):
    def __init__(self, message: str):
        super().__init__("conflict", message)


class InvalidIdentityAppError(AppError):
    def __init__(self, message: str):
        super().__init__("invalid_identity", message)


class RateLimitedAppError(AppError):
    def __init__(self, message: str):
        super().__init__("rate_limited", message)


class UnauthorizedAppError(AppError):
    def __init__(self, message: str):
        super().__init__("unauthorized", message)
