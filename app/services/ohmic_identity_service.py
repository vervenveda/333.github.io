"""Private 333/Bunya client for OHMIC HOLLO identity and phone-number authority."""

from __future__ import annotations

import os
from typing import Any
from uuid import UUID

import httpx

from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError, ServiceError, ValidationServiceError

OHMIC_IDENTITY_TIMEOUT_SECONDS = 8.0

class IdentityAuthorityUnavailableError(ServiceError):
    status_code = 503
    code = "identity_authority_unavailable"


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


async def _call(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not _upstream_url() or len(_gateway_token()) < 32:
        raise IdentityAuthorityUnavailableError("The sovereign OHMIC identity authority is not configured.")
    endpoint = f"{_upstream_url()}/api/v1/ohmic/identity/{action}"
    headers = {"Authorization": f"Bearer {_gateway_token()}", "Content-Type": "application/json", "Accept": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=OHMIC_IDENTITY_TIMEOUT_SECONDS) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise IdentityAuthorityUnavailableError("The sovereign OHMIC identity authority is unreachable.") from exc
    try:
        body = response.json()
    except ValueError as exc:
        raise IdentityAuthorityUnavailableError("The sovereign OHMIC identity authority returned an invalid response.") from exc
    message = str(body.get("message") or "The identity request could not be completed.")
    if response.status_code >= 500:
        raise IdentityAuthorityUnavailableError("The sovereign OHMIC identity authority is unavailable.")
    if response.status_code == 409:
        raise ConflictError(message)
    if response.status_code == 404:
        raise NotFoundError(message)
    if response.status_code in {401, 403}:
        raise AuthenticationError(message)
    if response.status_code == 422:
        raise ValidationServiceError(message)
    if response.status_code >= 400 or not body.get("ok"):
        raise ServiceError(message)
    return body


def _profile_payload(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "displayName": profile.get("display_name"),
        "handle": profile.get("handle"),
        "bio": profile.get("bio"),
        "avatarUrl": profile.get("avatar_url"),
        "visibility": profile.get("visibility", "members"),
    }


def _number_payload(number: dict[str, Any]) -> dict[str, Any]:
    return {
        "choice": number.get("choice"),
        "existingNumber": number.get("existing_number"),
        "makePrimary": number.get("make_primary", True),
    }


async def enroll_identity(*, member_id: UUID, profile: dict[str, Any], number: dict[str, Any]) -> dict[str, Any]:
    return await _call("enroll", {"schema": "ohmic-identity-enroll", "memberId": str(member_id), "profile": _profile_payload(profile), "number": _number_payload(number)})


async def get_profile(*, member_id: UUID) -> dict[str, Any]:
    body = await _call("profile-get", {"schema": "ohmic-profile-get", "memberId": str(member_id)})
    return dict(body["profile"])


async def update_profile(*, member_id: UUID, changes: dict[str, Any]) -> dict[str, Any]:
    mapped: dict[str, Any] = {}
    for source, target in {"display_name":"displayName", "handle":"handle", "bio":"bio", "avatar_url":"avatarUrl", "visibility":"visibility"}.items():
        if source in changes:
            value = changes[source]
            mapped[target] = getattr(value, "value", value)
    body = await _call("profile-update", {"schema": "ohmic-profile-update", "memberId": str(member_id), "changes": mapped})
    return dict(body["profile"])


async def list_numbers(*, member_id: UUID) -> list[dict[str, Any]]:
    body = await _call("numbers-list", {"schema": "ohmic-numbers-list", "memberId": str(member_id)})
    return [dict(item) for item in body.get("numbers", [])]


async def add_number(*, member_id: UUID, number: dict[str, Any]) -> dict[str, Any]:
    body = await _call("number-add", {"schema": "ohmic-number-add", "memberId": str(member_id), "number": _number_payload(number)})
    return dict(body["number"])
