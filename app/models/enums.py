"""Shared persisted status values."""

from enum import StrEnum


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DISABLED = "disabled"


class ProfileVisibility(StrEnum):
    PRIVATE = "private"
    MEMBERS = "members"
    PUBLIC = "public"


class NumberKind(StrEnum):
    EXISTING = "existing"
    NETWORK = "network"
    SERVICE = "service"


class NumberStatus(StrEnum):
    PROVISIONAL = "provisional"
    PENDING_VERIFICATION = "pending_verification"
    VERIFIED = "verified"
    RESERVED = "reserved"
    REVOKED = "revoked"


class EmailApplicationStatus(StrEnum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
