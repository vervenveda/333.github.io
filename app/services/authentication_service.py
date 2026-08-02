"""Registration, sign-in, token rotation, and logout."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.exceptions import AuthenticationError, ConflictError
from app.core.permissions import Role
from app.core.security import (
    create_access_token,
    fingerprint,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    password_needs_rehash,
    utc_now,
    verify_password,
)
from app.models.enums import UserStatus
from app.models.refresh_session import RefreshSession
from app.models.user import User
from app.services.audit_service import record_audit


@dataclass(frozen=True, slots=True)
class IssuedTokens:
    access_token: str
    refresh_token: str
    access_expires_at: object
    refresh_expires_at: object
    user: User


def normalize_email(email: str) -> str:
    return email.strip().casefold()


async def register_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    request_id: str | None = None,
    ip_address: str | None = None,
) -> User:
    normalized = normalize_email(email)
    existing = await session.scalar(select(User).where(User.email == normalized))
    if existing:
        raise ConflictError("An account with that email already exists.")

    user = User(
        email=normalized,
        password_hash=hash_password(password),
        status=UserStatus.ACTIVE.value,
        role=Role.MEMBER.value,
        email_verified=False,
        is_active=True,
    )
    session.add(user)

    try:
        await session.flush()
        await record_audit(
            session,
            actor_user_id=user.id,
            event_type="account.registered",
            resource_type="user",
            resource_id=str(user.id),
            request_id=request_id,
            ip_address_hash=fingerprint(ip_address),
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("An account with that email already exists.") from exc

    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession,
    *,
    email: str,
    password: str,
    request_id: str | None = None,
    ip_address: str | None = None,
) -> User:
    normalized = normalize_email(email)
    user = await session.scalar(select(User).where(User.email == normalized))
    now = utc_now()

    if not user:
        raise AuthenticationError("The email or password is incorrect.")
    if not user.is_active or user.status != UserStatus.ACTIVE.value:
        raise AuthenticationError("This account is not available.")
    if user.locked_until and user.locked_until > now:
        raise AuthenticationError("This account is temporarily locked.")

    if not verify_password(password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.login_max_attempts:
            user.locked_until = now + timedelta(
                minutes=settings.login_lock_minutes
            )
            user.failed_login_attempts = 0
        await record_audit(
            session,
            actor_user_id=user.id,
            event_type="authentication.failed",
            resource_type="user",
            resource_id=str(user.id),
            outcome="failure",
            request_id=request_id,
            ip_address_hash=fingerprint(ip_address),
        )
        await session.commit()
        raise AuthenticationError("The email or password is incorrect.")

    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)

    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = now

    await record_audit(
        session,
        actor_user_id=user.id,
        event_type="authentication.succeeded",
        resource_type="user",
        resource_id=str(user.id),
        request_id=request_id,
        ip_address_hash=fingerprint(ip_address),
    )
    await session.commit()
    await session.refresh(user)
    return user


async def issue_token_pair(
    session: AsyncSession,
    *,
    user: User,
    device_name: str | None,
    user_agent: str | None,
    ip_address: str | None,
    request_id: str | None = None,
) -> IssuedTokens:
    access_token, access_expires_at = create_access_token(
        user_id=user.id,
        role=user.role,
    )
    refresh_token = generate_refresh_token()
    refresh_expires_at = utc_now() + timedelta(days=settings.refresh_token_days)

    refresh_session = RefreshSession(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=refresh_expires_at,
        device_name=device_name,
        user_agent_hash=fingerprint(user_agent),
        ip_address_hash=fingerprint(ip_address),
    )
    session.add(refresh_session)
    await record_audit(
        session,
        actor_user_id=user.id,
        event_type="session.created",
        resource_type="refresh_session",
        request_id=request_id,
        ip_address_hash=fingerprint(ip_address),
        details={"device_name": device_name or "unspecified"},
    )
    await session.commit()

    return IssuedTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        access_expires_at=access_expires_at,
        refresh_expires_at=refresh_expires_at,
        user=user,
    )


async def rotate_refresh_token(
    session: AsyncSession,
    *,
    refresh_token: str,
    device_name: str | None,
    user_agent: str | None,
    ip_address: str | None,
    request_id: str | None = None,
) -> IssuedTokens:
    token_hash = hash_refresh_token(refresh_token)
    refresh_session = await session.scalar(
        select(RefreshSession)
        .options(selectinload(RefreshSession.user))
        .where(RefreshSession.token_hash == token_hash)
    )
    now = utc_now()

    if (
        not refresh_session
        or refresh_session.revoked_at is not None
        or refresh_session.expires_at <= now
    ):
        raise AuthenticationError("The refresh session is invalid or expired.")

    user = refresh_session.user
    if not user.is_active or user.status != UserStatus.ACTIVE.value:
        raise AuthenticationError("This account is not available.")

    refresh_session.revoked_at = now
    refresh_session.last_used_at = now

    access_token, access_expires_at = create_access_token(
        user_id=user.id,
        role=user.role,
    )
    new_refresh_token = generate_refresh_token()
    new_refresh_expires_at = now + timedelta(days=settings.refresh_token_days)

    session.add(
        RefreshSession(
            user_id=user.id,
            token_hash=hash_refresh_token(new_refresh_token),
            expires_at=new_refresh_expires_at,
            device_name=device_name or refresh_session.device_name,
            user_agent_hash=fingerprint(user_agent),
            ip_address_hash=fingerprint(ip_address),
        )
    )
    await record_audit(
        session,
        actor_user_id=user.id,
        event_type="session.rotated",
        resource_type="refresh_session",
        resource_id=str(refresh_session.id),
        request_id=request_id,
        ip_address_hash=fingerprint(ip_address),
    )
    await session.commit()

    return IssuedTokens(
        access_token=access_token,
        refresh_token=new_refresh_token,
        access_expires_at=access_expires_at,
        refresh_expires_at=new_refresh_expires_at,
        user=user,
    )


async def revoke_refresh_token(
    session: AsyncSession,
    *,
    refresh_token: str,
    request_id: str | None = None,
) -> bool:
    token_hash = hash_refresh_token(refresh_token)
    refresh_session = await session.scalar(
        select(RefreshSession).where(RefreshSession.token_hash == token_hash)
    )
    if not refresh_session:
        return False

    if refresh_session.revoked_at is None:
        refresh_session.revoked_at = utc_now()
        await record_audit(
            session,
            actor_user_id=refresh_session.user_id,
            event_type="session.revoked",
            resource_type="refresh_session",
            resource_id=str(refresh_session.id),
            request_id=request_id,
        )
        await session.commit()
    return True
