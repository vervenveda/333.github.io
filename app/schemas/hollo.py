"""HOLLO enrollment and network-number schemas."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field, model_validator

from app.schemas.common import ApiModel
from app.schemas.profile import ProfileCreate, ProfileResponse


class NumberChoice(StrEnum):
    EXISTING = "existing"
    NETWORK = "network"


class NumberRequest(ApiModel):
    choice: NumberChoice
    existing_number: str | None = Field(default=None, max_length=32)
    make_primary: bool = True

    @model_validator(mode="after")
    def validate_choice(self) -> "NumberRequest":
        if self.choice is NumberChoice.EXISTING and not self.existing_number:
            raise ValueError("existing_number is required for an existing number.")
        if self.choice is NumberChoice.NETWORK and self.existing_number:
            raise ValueError(
                "existing_number must be omitted when requesting a 333 number."
            )
        return self


class NetworkNumberResponse(ApiModel):
    id: UUID
    user_id: UUID
    number: str
    kind: str
    status: str
    is_primary: bool
    verification_method: str | None
    verified_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EnrollmentRequest(ApiModel):
    profile: ProfileCreate
    number: NumberRequest


class EnrollmentResponse(ApiModel):
    profile: ProfileResponse
    number: NetworkNumberResponse
    notice: str
