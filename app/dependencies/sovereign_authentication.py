"""Resolve a 333 member through the sovereign OHMIC member authority.

Bearer/session tokens are verified by the 333 Network. Member existence, status,
role, and permissions are then confirmed by the Secure Server/OHMIC encrypted
member registry. No SQL database is consulted by this dependency.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from uuid import UUID

import httpx
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings
from app.core.exceptions import AuthenticationError, ServiceError
from app.core.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)
OHMIC_AUTH_TIMEOUT_SECONDS = 6.0


class MemberAuthorityUnavailableError(ServiceError):
    status_code = 503
    code = "member_authority_unavailable"


@dataclass(frozen=True, slots=True)
class SovereignMember:
    id: UUID
    role: str
    status: str
    permissions: tuple[str, ...]


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


def _authority_ready() -> bool:
    return bool(_upstream_url()) and len(_gateway_token()) >= 32


async def get_current_sovereign_member(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> SovereignMember:
    """Validate a 333 access token, then confirm membership in OHMIC."""
    token: str | None = None

    if credentials is not None and credentials.scheme.casefold() == "bearer":
        token = credentials.credentials

    if not token:
        token = request.cookies.get(settings.cookie_name)

    if not token:
        raise AuthenticationError("Authentication is required.")

    payload = decode_access_token(token)
    try:
        member_id = UUID(str(payload["sub"]))
    except (KeyError, ValueError) as exc:
        raise AuthenticationError("The access token subject is invalid.") from exc

    if not _authority_ready():
        raise MemberAuthorityUnavailableError(
            "The sovereign OHMIC member authority is not configured."
        )

    endpoint = f"{_upstream_url()}/api/v1/ohmic/member-auth"
    headers = {
        "Authorization": f"Bearer {_gateway_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    request_id = getattr(request.state, "request_id", "") or ""
    if request_id:
        headers["X-Request-Id"] = str(request_id)[:128]

    body = {
        "schema": "ohmic-member-auth-check",
        "memberId": str(member_id),
    }

    try:
        async with httpx.AsyncClient(timeout=OHMIC_AUTH_TIMEOUT_SECONDS) as client:
            response = await client.post(endpoint, headers=headers, json=body)
    except httpx.RequestError as exc:
        raise MemberAuthorityUnavailableError(
            "The sovereign OHMIC member authority is unreachable."
        ) from exc

    try:
        result = response.json()
    except ValueError as exc:
        raise MemberAuthorityUnavailableError(
            "The sovereign OHMIC member authority returned an invalid response."
        ) from exc

    if response.status_code >= 500:
        raise MemberAuthorityUnavailableError(
            "The sovereign OHMIC member authority is unavailable."
        )

    if response.status_code >= 400:
        raise AuthenticationError("Member verification was not accepted.")

    if not result.get("ok") or not result.get("active"):
        raise AuthenticationError("This account is not available.")

    member = result.get("member") or {}
    try:
        confirmed_id = UUID(str(member["id"]))
    except (KeyError, ValueError) as exc:
        raise MemberAuthorityUnavailableError(
            "The sovereign member record is invalid."
        ) from exc

    if confirmed_id != member_id:
        raise MemberAuthorityUnavailableError(
            "The sovereign member authority returned a mismatched identity."
        )

    role = str(member.get("role") or "member").strip()[:80] or "member"
    status = str(member.get("status") or "active").strip()[:40] or "active"
    raw_permissions = member.get("permissions")
    permissions = tuple(
        str(item).strip()[:120]
        for item in (raw_permissions if isinstance(raw_permissions, list) else [])
        if str(item).strip()
    )

    return SovereignMember(
        id=confirmed_id,
        role=role,
        status=status,
        permissions=permissions,
    )
