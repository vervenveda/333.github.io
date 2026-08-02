"""E=Ven Mail application schemas."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.schemas.common import ApiModel

LOCAL_PART_PATTERN = r"^[a-z0-9](?:[a-z0-9._-]{0,62}[a-z0-9])?$"


class EmailApplicationCreate(ApiModel):
    requested_local_part: str = Field(
        min_length=1,
        max_length=64,
        pattern=LOCAL_PART_PATTERN,
    )
    requested_domain: str = Field(min_length=3, max_length=255)
    alternate_contact_email: EmailStr | None = None
    purpose: str | None = Field(default=None, max_length=2000)
    applicant_notes: str | None = Field(default=None, max_length=4000)

    @field_validator("requested_local_part", "requested_domain", mode="before")
    @classmethod
    def normalize_address_parts(cls, value: object) -> object:
        return value.strip().casefold() if isinstance(value, str) else value

    @field_validator("purpose", "applicant_notes", mode="before")
    @classmethod
    def trim_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class EmailApplicationResponse(ApiModel):
    id: UUID
    reference: str
    user_id: UUID
    requested_local_part: str
    requested_domain: str
    requested_address: str
    alternate_contact_email: EmailStr | None
    purpose: str | None
    status: str
    applicant_notes: str | None
    administrator_notes: str | None
    submitted_at: datetime
    reviewed_at: datetime | None
    reviewed_by_user_id: UUID | None
    created_at: datetime
    updated_at: datetime


class ReviewDecision(StrEnum):
    APPROVE = "approve"
    REJECT = "reject"
    MARK_UNDER_REVIEW = "mark_under_review"


class EmailApplicationReview(ApiModel):
    decision: ReviewDecision
    administrator_notes: str | None = Field(default=None, max_length=4000)
