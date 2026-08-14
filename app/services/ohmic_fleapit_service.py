"""Private Bunya client for the OHMIC FleaPit member-library authority."""
from __future__ import annotations

import os
from typing import Any
from uuid import UUID

import httpx

from app.core.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ServiceError,
    ValidationServiceError,
)

OHMIC_FLEAPIT_TIMEOUT_SECONDS = 8.0


class FleaPitAuthorityUnavailableError(ServiceError):
    status_code = 503
    code = "fleapit_authority_unavailable"


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


async def _call(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not _upstream_url() or len(_gateway_token()) < 32:
        raise FleaPitAuthorityUnavailableError(
            "The sovereign OHMIC FleaPit authority is not configured."
        )

    endpoint = f"{_upstream_url()}/api/v1/ohmic/fleapit/{action}"
    headers = {
        "Authorization": f"Bearer {_gateway_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=OHMIC_FLEAPIT_TIMEOUT_SECONDS) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise FleaPitAuthorityUnavailableError(
            "The sovereign OHMIC FleaPit authority is unreachable."
        ) from exc

    try:
        body = response.json()
    except ValueError as exc:
        raise FleaPitAuthorityUnavailableError(
            "The sovereign OHMIC FleaPit authority returned an invalid response."
        ) from exc

    message = str(body.get("message") or "The FleaPit request could not be completed.")
    if response.status_code >= 500:
        raise FleaPitAuthorityUnavailableError(
            "The sovereign OHMIC FleaPit authority is unavailable."
        )
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


async def fleapit_status() -> dict[str, Any]:
    return await _call("status", {"schema": "ohmic-fleapit-status"})


async def get_state(*, member_id: UUID) -> dict[str, Any]:
    return await _call(
        "state-get",
        {"schema": "ohmic-fleapit-state-get", "memberId": str(member_id)},
    )


async def put_state(
    *,
    member_id: UUID,
    state: dict[str, Any],
    base_revision: int | None,
    reason: str,
) -> dict[str, Any]:
    return await _call(
        "state-put",
        {
            "schema": "ohmic-fleapit-state-put",
            "memberId": str(member_id),
            "state": state,
            "baseRevision": base_revision,
            "reason": reason,
        },
    )


async def create_snapshot(*, member_id: UUID, reason: str) -> dict[str, Any]:
    return await _call(
        "snapshot-create",
        {
            "schema": "ohmic-fleapit-snapshot-create",
            "memberId": str(member_id),
            "reason": reason,
        },
    )


async def list_snapshots(*, member_id: UUID) -> dict[str, Any]:
    return await _call(
        "snapshot-list",
        {"schema": "ohmic-fleapit-snapshot-list", "memberId": str(member_id)},
    )


async def restore_snapshot(*, member_id: UUID, snapshot_id: str) -> dict[str, Any]:
    return await _call(
        "snapshot-restore",
        {
            "schema": "ohmic-fleapit-snapshot-restore",
            "memberId": str(member_id),
            "snapshotId": snapshot_id,
        },
    )
