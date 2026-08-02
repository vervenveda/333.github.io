"""Role-based FastAPI dependencies."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends

from app.core.exceptions import PermissionDeniedError
from app.core.permissions import Role, role_is_allowed
from app.dependencies.authentication import get_current_user
from app.models.user import User


def require_roles(*roles: Role) -> Callable[..., User]:
    allowed = set(roles)

    async def dependency(
        user: User = Depends(get_current_user),
    ) -> User:
        if not role_is_allowed(user.role, allowed):
            raise PermissionDeniedError(
                "This account does not have permission for that action."
            )
        return user

    return dependency
