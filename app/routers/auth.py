"""Sovereign 333 account registration, login, refresh, logout, and current member."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.config import settings
from app.core.rate_limits import rate_limiter
from app.core.security import create_access_token, validate_password_strength
from app.dependencies.sovereign_authentication import (
    SovereignMember,
    get_current_sovereign_member,
)
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPairResponse,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.ohmic_account_service import (
    get_account,
    login_account,
    logout_account,
    refresh_account,
    register_account,
)

router = APIRouter()


def _request_ip(request: Request) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else None


def _parse_datetime(value: object) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)


def _member_response(member: dict[str, object]) -> UserResponse:
    return UserResponse(
        id=UUID(str(member["id"])),
        email=str(member["email"]),
        status=str(member.get("status") or "active"),
        role=str(member.get("role") or "member"),
        email_verified=bool(member.get("emailVerified")),
        is_active=bool(member.get("isActive")),
        created_at=_parse_datetime(member.get("createdAt")),
        updated_at=_parse_datetime(member.get("updatedAt")),
    )


def _token_response(authority_payload: dict[str, object]) -> TokenPairResponse:
    member = _member_response(dict(authority_payload["member"]))
    access_token, access_expires_at = create_access_token(
        user_id=member.id,
        role=member.role,
    )
    return TokenPairResponse(
        access_token=access_token,
        refresh_token=str(authority_payload["refreshToken"]),
        access_expires_at=access_expires_at,
        refresh_expires_at=_parse_datetime(authority_payload["refreshExpiresAt"]),
        user=member,
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
async def register(payload: RegisterRequest, request: Request) -> UserResponse:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"register:{ip or 'unknown'}",
        limit=settings.registration_rate_limit,
        window_seconds=3600,
    )
    password = payload.password.get_secret_value()
    validate_password_strength(password)
    member = await register_account(email=str(payload.email), password=password)
    return _member_response(member)


@router.post("/login", response_model=TokenPairResponse)
async def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
) -> TokenPairResponse:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"login:{ip or 'unknown'}",
        limit=settings.login_rate_limit,
        window_seconds=900,
    )
    authority = await login_account(
        email=str(payload.email),
        password=payload.password.get_secret_value(),
    )
    tokens = _token_response(authority)
    _set_access_cookie(response, tokens.access_token)
    return tokens


@router.post("/refresh", response_model=TokenPairResponse)
async def refresh(
    payload: RefreshRequest,
    request: Request,
    response: Response,
) -> TokenPairResponse:
    ip = _request_ip(request)
    await rate_limiter.enforce(
        key=f"refresh:{ip or 'unknown'}",
        limit=settings.refresh_rate_limit,
        window_seconds=900,
    )
    authority = await refresh_account(
        refresh_token=payload.refresh_token.get_secret_value()
    )
    tokens = _token_response(authority)
    _set_access_cookie(response, tokens.access_token)
    return tokens


@router.post("/logout", response_model=MessageResponse)
async def logout(
    payload: LogoutRequest,
    response: Response,
) -> MessageResponse:
    await logout_account(refresh_token=payload.refresh_token.get_secret_value())
    _clear_access_cookie(response)
    return MessageResponse(message="The OHMIC refresh session has been revoked.")


@router.get("/me", response_model=UserResponse)
async def me(
    member: SovereignMember = Depends(get_current_sovereign_member),
) -> UserResponse:
    account = await get_account(member_id=member.id)
    return _member_response(account)
