"""Account registration, login, refresh, logout, and current user."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_database_session
from app.core.rate_limits import rate_limiter
from app.dependencies.authentication import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPairResponse,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.authentication_service import (
    authenticate_user,
    issue_token_pair,
    register_user,
    revoke_refresh_token,
    rotate_refresh_token,
)

router = APIRouter()


def _request_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else None


def _token_response(tokens) -> TokenPairResponse:
    return TokenPairResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        access_expires_at=tokens.access_expires_at,
        refresh_expires_at=tokens.refresh_expires_at,
        user=UserResponse.model_validate(tokens.user),
    )


def _set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key=settings.cookie_name,
        value=access_token,
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain or None,
        path="/",
    )


def _clear_access_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.cookie_name,
        domain=settings.cookie_domain or None,
        path="/",
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    request: Request,
    session: AsyncSession = Depends(get_database_session),
) -> User:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"register:{ip or 'unknown'}",
        limit=settings.registration_rate_limit,
        window_seconds=3600,
    )
    return await register_user(
        session,
        email=str(payload.email),
        password=payload.password.get_secret_value(),
        request_id=getattr(request.state, "request_id", None),
        ip_address=ip,
    )


@router.post("/login", response_model=TokenPairResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_database_session),
) -> TokenPairResponse:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"login:{ip or 'unknown'}",
        limit=settings.login_rate_limit,
        window_seconds=900,
    )
    user = await authenticate_user(
        session,
        email=str(payload.email),
        password=payload.password.get_secret_value(),
        request_id=getattr(request.state, "request_id", None),
        ip_address=ip,
    )
    tokens = await issue_token_pair(
        session,
        user=user,
        device_name=payload.device_name,
        user_agent=request.headers.get("user-agent"),
        ip_address=ip,
        request_id=getattr(request.state, "request_id", None),
    )
    _set_access_cookie(response, tokens.access_token)
    return _token_response(tokens)


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(
    payload: RefreshRequest,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_database_session),
) -> TokenPairResponse:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"refresh:{ip or 'unknown'}",
        limit=settings.refresh_rate_limit,
        window_seconds=900,
    )
    tokens = await rotate_refresh_token(
        session,
        refresh_token=payload.refresh_token.get_secret_value(),
        device_name=payload.device_name,
        user_agent=request.headers.get("user-agent"),
        ip_address=ip,
        request_id=getattr(request.state, "request_id", None),
    )
    _set_access_cookie(response, tokens.access_token)
    return _token_response(tokens)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    payload: LogoutRequest,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_database_session),
) -> MessageResponse:
    await revoke_refresh_token(
        session,
        refresh_token=payload.refresh_token.get_secret_value(),
        request_id=getattr(request.state, "request_id", None),
    )
    _clear_access_cookie(response)
    return MessageResponse(message="The refresh session has been revoked.")


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)) -> User:
    return user
