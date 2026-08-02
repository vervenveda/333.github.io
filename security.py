"""Password, JWT, refresh-token, and fingerprint utilities."""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import AuthenticationError, ValidationServiceError

PASSWORD_HASHER = PasswordHasher(
    time_cost=3,
    memory_cost=65_536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
)

COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456789",
    "qwerty123",
    "letmein",
    "welcome",
    "admin123",
}


def utc_now() -> datetime:
    return datetime.now(UTC)


def validate_password_strength(password: str) -> None:
    """Apply a practical baseline without silently modifying passwords."""
    minimum = settings.minimum_password_length
    if len(password) < minimum:
        raise ValidationServiceError(
            f"Password must contain at least {minimum} characters."
        )
    if len(password) > 512:
        raise ValidationServiceError("Password is too long.")
    if password.casefold() in COMMON_PASSWORDS:
        raise ValidationServiceError("Choose a less common password.")
    categories = sum(
        bool(pattern.search(password))
        for pattern in (
            re.compile(r"[a-z]"),
            re.compile(r"[A-Z]"),
            re.compile(r"\d"),
            re.compile(r"[^A-Za-z0-9]"),
        )
    )
    if categories < 3:
        raise ValidationServiceError(
            "Use at least three of: lowercase, uppercase, numbers, or symbols."
        )


def hash_password(password: str) -> str:
    validate_password_strength(password)
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return PASSWORD_HASHER.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def password_needs_rehash(password_hash: str) -> bool:
    try:
        return PASSWORD_HASHER.check_needs_rehash(password_hash)
    except InvalidHashError:
        return True


def create_access_token(
    *,
    user_id: UUID,
    role: str,
    extra_claims: dict[str, Any] | None = None,
) -> tuple[str, datetime]:
    issued_at = utc_now()
    expires_at = issued_at + timedelta(minutes=settings.access_token_minutes)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "jti": str(uuid4()),
        "iat": int(issued_at.timestamp()),
        "nbf": int(issued_at.timestamp()),
        "exp": int(expires_at.timestamp()),
        "iss": settings.jwt_issuer,
        "aud": settings.jwt_audience,
    }
    if extra_claims:
        payload.update(extra_claims)

    token = jwt.encode(
        payload,
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.token_signing_algorithm,
    )
    return token, expires_at


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.token_signing_algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options={"require_sub": True, "require_exp": True},
        )
    except JWTError as exc:
        raise AuthenticationError("The access token is invalid or expired.") from exc

    if payload.get("type") != "access":
        raise AuthenticationError("The supplied token is not an access token.")
    return payload


def generate_refresh_token() -> str:
    """Generate an opaque refresh token; only its hash is persisted."""
    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_opaque_token(length: int = 48) -> str:
    return secrets.token_urlsafe(length)


def hash_opaque_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def fingerprint(value: str | None) -> str | None:
    """Create a non-reversible keyed fingerprint for IP/user-agent metadata."""
    if not value:
        return None
    secret = settings.session_secret.get_secret_value().encode("utf-8")
    return hmac.new(secret, value.encode("utf-8"), hashlib.sha256).hexdigest()
