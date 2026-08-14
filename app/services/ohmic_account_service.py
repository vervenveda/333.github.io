"""Private Bunya client for the OHMIC sovereign account authority."""

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

OHMIC_ACCOUNT_TIMEOUT_SECONDS = 8.0


class AccountAuthorityUnavailableError(ServiceError):
    status_code = 503
    code = "account_authority_unavailable"


def _upstream_url() -> str:
    return os.getenv("OHMIC_UPSTREAM_URL", "").strip().rstrip("/")


def _gateway_token() -> str:
    return os.getenv("OHMIC_GATEWAY_TOKEN", "").strip()


def _ready() -> bool:
    return bool(_upstream_url()) and len(_gateway_token()) >= 32


async def _call(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not _ready():
        raise AccountAuthorityUnavailableError(
            "The sovereign OHMIC account authority is not configured."
        )

    endpoint = f"{_upstream_url()}/api/v1/ohmic/account/{action}"
    headers = {
        "Authorization": f"Bearer {_gateway_token()}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=OHMIC_ACCOUNT_TIMEOUT_SECONDS) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
    except httpx.RequestError as exc:
        raise AccountAuthorityUnavailableError(
            "The sovereign OHMIC account authority is unreachable."
        ) from exc

    try:
        body = response.json()
    except ValueError as exc:
        raise AccountAuthorityUnavailableError(
            "The sovereign OHMIC account authority returned an invalid response."
        ) from exc

    message = str(body.get("message") or "The account request could not be completed.")
    code = str(body.get("error") or "")

    if response.status_code >= 500:
        raise AccountAuthorityUnavailableError(
            "The sovereign OHMIC account authority is unavailable."
        )
    if response.status_code == 409:
        raise ConflictError(message)
    if response.status_code == 404:
        raise NotFoundError(message)
    if response.status_code in {401, 403}:
        raise AuthenticationError(message)
    if response.status_code == 422:
        raise ValidationServiceError(message, details={"authority_code": code})
    if response.status_code >= 400 or not body.get("ok"):
        raise ServiceError(message)

    return body


async def register_account(*, email: str, password: str) -> dict[str, Any]:
    body = await _call(
        "register",
        {
            "schema": "ohmic-account-register",
            "email": email,
            "password": password,
        },
    )
    return dict(body["member"])


async def login_account(*, email: str, password: str) -> dict[str, Any]:
    return await _call(
        "login",
        {
            "schema": "ohmic-account-login",
            "email": email,
            "password": password,
        },
    )


async def refresh_account(*, refresh_token: str) -> dict[str, Any]:
    return await _call(
        "refresh",
        {
            "schema": "ohmic-account-refresh",
            "refreshToken": refresh_token,
        },
    )


async def logout_account(*, refresh_token: str) -> bool:
    body = await _call(
        "logout",
        {
            "schema": "ohmic-account-logout",
            "refreshToken": refresh_token,
        },
    )
    return bool(body.get("revoked"))


async def get_account(*, member_id: UUID) -> dict[str, Any]:
    body = await _call(
        "get",
        {
            "schema": "ohmic-account-get",
            "memberId": str(member_id),
        },
    )
    return dict(body["member"])
