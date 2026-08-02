"""Role definitions and authorization helpers."""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    MEMBER = "member"
    MODERATOR = "moderator"
    MAIL_ADMIN = "mail_admin"
    INFRASTRUCTURE_ADMIN = "infrastructure_admin"
    ADMINISTRATOR = "administrator"


ROLE_RANK: dict[Role, int] = {
    Role.MEMBER: 10,
    Role.MODERATOR: 20,
    Role.MAIL_ADMIN: 30,
    Role.INFRASTRUCTURE_ADMIN: 30,
    Role.ADMINISTRATOR: 100,
}


def normalize_role(value: str) -> Role:
    try:
        return Role(value)
    except ValueError:
        return Role.MEMBER


def role_is_allowed(current: str, allowed: set[Role]) -> bool:
    role = normalize_role(current)
    if role is Role.ADMINISTRATOR:
        return True
    return role in allowed
