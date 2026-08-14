"""Fail-closed CSRF adapter for FleaPit cookie-authenticated writes.

The current sovereign local backbone already owns the canonical CSRF verifier.
This adapter deliberately refuses to authorize browser writes if that verifier
is unavailable or its exported dependency cannot be resolved.
"""
from __future__ import annotations

from importlib import import_module
from typing import Any, Awaitable, Callable

from fastapi import HTTPException, Request, status

_CANDIDATE_EXPORTS = (
    "require_csrf",
    "require_sovereign_csrf",
    "verify_csrf",
    "verify_csrf_request",
    "require_csrf_protection",
)


def _resolve() -> Callable[..., Any] | None:
    try:
        module = import_module("app.dependencies.sovereign_csrf")
    except (ImportError, ModuleNotFoundError):
        return None
    for name in _CANDIDATE_EXPORTS:
        candidate = getattr(module, name, None)
        if callable(candidate):
            return candidate
    return None


async def require_fleapit_csrf(request: Request) -> None:
    """Delegate to the sovereign CSRF authority or fail closed.

    Bearer-client bypasses, origin validation, token binding, and session/JTI
    semantics remain the responsibility of the canonical sovereign verifier.
    """
    verifier = _resolve()
    if verifier is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sovereign CSRF protection is not available; FleaPit writes are disabled.",
        )

    result = verifier(request)
    if isinstance(result, Awaitable):
        await result
