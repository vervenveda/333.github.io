"""Member profile schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.models.enums import ProfileVisibility
from app.schemas.common import ApiModel

HANDLE_PATTERN = r"^[a-z0-9](?:[a-z0-9._-]{1,28}[a-z0-9])?$"


class ProfileCreate(ApiModel):
    display_name: str = Field(min_length=1, max_length=120)
    handle: str = Field(min_length=3, max_length=30, pattern=HANDLE_PATTERN)
    bio: str | None = Field(default=None, max_length=2000)
    avatar_url: str | None = Field(default=None, max_length=2048)
    visibility: ProfileVisibility = ProfileVisibility.MEMBERS

    @field_validator("display_name", "bio", mode="before")
    @classmethod
    def trim_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("handle", mode="before")
    @classmethod
    def normalize_handle(cls, value: object) -> object:
        return value.strip().casefold() if isinstance(value, str) else value


class ProfileUpdate(ApiModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    handle: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=HANDLE_PATTERN,
    )
    bio: str | None = Field(default=None, max_length=2000)
    avatar_url: str | None = Field(default=None, max_length=2048)
    visibility: ProfileVisibility | None = None

    @field_validator("display_name", "bio", mode="before")
    @classmethod
    def trim_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("handle", mode="before")
    @classmethod
    def normalize_handle(cls, value: object) -> object:
        return value.strip().casefold() if isinstance(value, str) else value


class ProfileResponse(ApiModel):
    id: UUID
    user_id: UUID
    display_name: str
    handle: str
    bio: str | None
    avatar_url: str | None
    visibility: str
    created_at: datetime
    updated_at: datetime
