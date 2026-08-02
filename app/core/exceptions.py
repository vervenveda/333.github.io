"""Application-safe service exceptions."""

from __future__ import annotations


class ServiceError(Exception):
    """Base error translated into a stable API response."""

    status_code = 400
    code = "service_error"

    def __init__(self, message: str, *, details: dict[str, object] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class AuthenticationError(ServiceError):
    status_code = 401
    code = "authentication_failed"


class PermissionDeniedError(ServiceError):
    status_code = 403
    code = "permission_denied"


class NotFoundError(ServiceError):
    status_code = 404
    code = "not_found"


class ConflictError(ServiceError):
    status_code = 409
    code = "conflict"


class ValidationServiceError(ServiceError):
    status_code = 422
    code = "validation_error"


class RateLimitError(ServiceError):
    status_code = 429
    code = "rate_limit_exceeded"
