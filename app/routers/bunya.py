"""Bunya root gateway for the 333 Network.

This router exposes a narrow public service registry and a member-authenticated
OHMIC Cloud sync bridge. It never accepts or exposes Secure Server admin secrets.
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import APIRouter, Depends, Request, status

from app.core.exceptions import ServiceError, ValidationServiceError
from app.dependencies.authentication import get_current_user
from app.models.user import User

router = APIRouter()


class GatewayUnavailableError(ServiceError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "gateway_unavailable"


class UpstreamGatewayError(ServiceError):
    status_code = status.HTTP_502_BAD_GATEWAY
    code = "upstream_gateway_error"


MAX_MEMBER_CLOUD_BYTES = 2 * 1024 * 1024
OHMIC_TIMEOUT_SECONDS = 12.0


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


def _gateway_ready() -> bool:
    return bool(_upstream_url()) and len(_gateway_token()) >= 32


@router.get("/status")
async def bunya_status() -> dict[str, Any]:
    """Describe the root connection without revealing private configuration."""
    return {
        "service": "Bunya",
        "role": "infrastructure-root",
        "network": "333 Network",
        "ohmic_cloud_gateway_configured": _gateway_ready(),
        "applications": [
            {"id": "bazaar-art", "label": "Bazaar Art", "role": "social-media-feed"},
            {"id": "even-mail", "label": "E=mail", "role": "mail"},
            {"id": "kansee", "label": "KANSEE", "role": "meeting-rooms"},
            {"id": "333", "label": "333", "role": "network-application"},
            {"id": "site", "label": "SIte", "role": "site-builder"},
            {
                "id": "weal",
                "label": "WEAL",
                "role": "future-domain-hosting",
                "state": "planned",
            },
        ],
    }


@router.get("/services")
async def service_registry() -> dict[str, Any]:
    """Return the activation registry used by the 333 Network shell."""
    return {
        "root": "Bunya",
        "network": "333 Network",
        "services": [
            {
                "id": "bazaar-art",
                "label": "Bazaar Art",
                "state": "frontend-ready",
                "purpose": "social-media-feed",
                "path": "/app/Bazaar_Art_Live_index.html",
            },
            {
                "id": "even-mail",
                "label": "E=mail",
                "state": "backend-partial",
                "purpose": "mail",
                "path": "/app/EVen_mail_index.html",
            },
            {
                "id": "kansee",
                "label": "KANSEE",
                "state": "frontend-ready",
                "purpose": "meeting-rooms",
                "path": "/app/KANSEE_333_meeting_rooms_index.html",
            },
            {
                "id": "333",
                "label": "333",
                "state": "active",
                "purpose": "network-application",
                "path": "/",
            },
            {
                "id": "site",
                "label": "SIte",
                "state": "frontend-ready",
                "purpose": "site-builder",
                "path": "/app/SIte_builder_index.html",
            },
            {
                "id": "weal",
                "label": "WEAL",
                "state": "planned",
                "purpose": "future-domain-hosting",
                "path": None,
            },
        ],
    }


@router.post("/cloud")
async def sync_ohmic_cloud(
    request: Request,
    user: User = Depends(get_current_user),
) -> dict[str, Any]:
    """Pass an authenticated member project to the trusted OHMIC/Next.js seam."""
    if not _gateway_ready():
        raise GatewayUnavailableError(
            "The OHMIC member-cloud gateway is not configured.",
            details={"state": "gateway_unavailable"},
        )

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_MEMBER_CLOUD_BYTES:
                raise ValidationServiceError("The OHMIC project payload is too large.")
        except ValueError:
            raise ValidationServiceError("Content-Length is invalid.")

    raw = await request.body()
    if len(raw) > MAX_MEMBER_CLOUD_BYTES:
        raise ValidationServiceError("The OHMIC project payload is too large.")

    try:
        payload = await request.json()
    except Exception as exc:
        raise ValidationServiceError("The OHMIC project payload must be valid JSON.") from exc

    if not isinstance(payload, dict) or payload.get("schema") != "ohmic-member-cloud-sync":
        raise ValidationServiceError("Unsupported OHMIC member-cloud schema.")

    request_id = getattr(request.state, "request_id", "") or ""
    upstream = f"{_upstream_url()}/api/v1/ohmic/member-cloud"

    headers = {
        "Authorization": f"Bearer {_gateway_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-333-User-Id": str(user.id),
    }
    if request_id:
        headers["X-Request-Id"] = str(request_id)[:128]

    try:
        async with httpx.AsyncClient(timeout=OHMIC_TIMEOUT_SECONDS) as client:
            response = await client.post(upstream, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise GatewayUnavailableError(
            "OHMIC Cloud is temporarily unreachable.",
            details={"state": "upstream_unreachable"},
        ) from exc

    try:
        body = response.json()
    except ValueError:
        body = {}

    if response.status_code >= 400:
        raise UpstreamGatewayError(
            "OHMIC Cloud did not accept the project.",
            details={
                "state": "upstream_rejected",
                "upstream_status": response.status_code,
            },
        )

    return {
        "ok": True,
        "project": body.get("project"),
        "revision": body.get("revision"),
        "storedAt": body.get("storedAt"),
        "gateway": "Bunya",
        "cloud": "OHMIC Foundry",
        "requestId": request_id or None,
    }
