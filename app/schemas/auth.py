"""Authentication schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field, SecretStr

from app.schemas.common import ApiModel


class RegisterRequest(ApiModel):
    email: EmailStr
    password: SecretStr


class LoginRequest(ApiModel):
    email: EmailStr
    password: SecretStr
    device_name: str | None = Field(default=None, max_length=120)


class RefreshRequest(ApiModel):
    refresh_token: SecretStr
    device_name: str | None = Field(default=None, max_length=120)


class LogoutRequest(ApiModel):
    refresh_token: SecretStr


class UserResponse(ApiModel):
    id: UUID
    email: EmailStr
    status: str
    role: str
    email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TokenPairResponse(ApiModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_expires_at: datetime
    refresh_expires_at: datetime
    user: UserResponse
