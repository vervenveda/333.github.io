"""Resolve the authenticated user from an access token."""

from __future__ import annotations

from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.core.exceptions import AuthenticationError
from app.core.security import decode_access_token
from app.models.enums import UserStatus
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_database_session),
) -> User:
    if credentials is None or credentials.scheme.casefold() != "bearer":
        raise AuthenticationError("Authentication is required.")

    payload = decode_access_token(credentials.credentials)
    try:
        user_id = UUID(str(payload["sub"]))
    except (KeyError, ValueError) as exc:
        raise AuthenticationError("The access token subject is invalid.") from exc

    user = await session.get(User, user_id)
    if (
        not user
        or not user.is_active
        or user.status != UserStatus.ACTIVE.value
    ):
        raise AuthenticationError("This account is not available.")
    return user
