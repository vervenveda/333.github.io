"""Private 333/Bunya client for the OHMIC Bazaar Art Live social-feed authority."""
from __future__ import annotations

import os
from typing import Any
from uuid import UUID

import httpx

from app.core.exceptions import AuthenticationError, ConflictError, NotFoundError, ServiceError, ValidationServiceError

OHMIC_BAZAAR_TIMEOUT_SECONDS = 8.0

class BazaarAuthorityUnavailableError(ServiceError):
    status_code = 503
    code = "bazaar_authority_unavailable"


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


async def _call(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not _upstream_url() or len(_gateway_token()) < 32:
        raise BazaarAuthorityUnavailableError("The sovereign OHMIC Bazaar authority is not configured.")
    endpoint = f"{_upstream_url()}/api/v1/ohmic/bazaar/{action}"
    headers = {"Authorization": f"Bearer {_gateway_token()}", "Content-Type": "application/json", "Accept": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=OHMIC_BAZAAR_TIMEOUT_SECONDS) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise BazaarAuthorityUnavailableError("The sovereign OHMIC Bazaar authority is unreachable.") from exc
    try:
        body = response.json()
    except ValueError as exc:
        raise BazaarAuthorityUnavailableError("The sovereign OHMIC Bazaar authority returned an invalid response.") from exc
    message = str(body.get("message") or "The Bazaar request could not be completed.")
    if response.status_code >= 500:
        raise BazaarAuthorityUnavailableError("The sovereign OHMIC Bazaar authority is unavailable.")
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


async def bazaar_status() -> dict[str, Any]:
    return await _call("status", {"schema": "ohmic-bazaar-status"})


async def create_post(*, member_id: UUID, post: dict[str, Any]) -> dict[str, Any]:
    return await _call("post-create", {"schema": "ohmic-bazaar-post-create", "memberId": str(member_id), "post": post})


async def list_feed(*, member_id: UUID, limit: int = 50, before: str | None = None) -> dict[str, Any]:
    return await _call("feed-list", {"schema": "ohmic-bazaar-feed-list", "memberId": str(member_id), "limit": limit, "before": before})


async def get_post(*, member_id: UUID, post_id: str) -> dict[str, Any]:
    return await _call("post-get", {"schema": "ohmic-bazaar-post-get", "memberId": str(member_id), "postId": post_id})


async def set_reaction(*, member_id: UUID, post_id: str, reaction: str) -> dict[str, Any]:
    return await _call("reaction-set", {"schema": "ohmic-bazaar-reaction-set", "memberId": str(member_id), "postId": post_id, "reaction": reaction})


async def add_comment(*, member_id: UUID, post_id: str, text: str) -> dict[str, Any]:
    return await _call("comment-add", {"schema": "ohmic-bazaar-comment-add", "memberId": str(member_id), "postId": post_id, "text": text})


async def delete_post(*, member_id: UUID, post_id: str) -> dict[str, Any]:
    return await _call("post-delete", {"schema": "ohmic-bazaar-post-delete", "memberId": str(member_id), "postId": post_id})
