"""FleaPit member-library gateway backed by encrypted OHMIC persistence."""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, field_validator

from app.dependencies.fleapit_csrf import require_fleapit_csrf
from app.dependencies.sovereign_authentication import (
    SovereignMember,
    get_current_sovereign_member,
)
from app.services.ohmic_fleapit_service import (
    create_snapshot,
    fleapit_status,
    get_state,
    list_snapshots,
    put_state,
    restore_snapshot,
)

router = APIRouter()

MAX_STATE_BYTES = 2 * 1024 * 1024
MAX_MEDIA = 500
MAX_RESOURCES = 200
MAX_QUEUE = 50
MAX_FAVORITES = 500


class FleaPitState(BaseModel):
    schemaVersion: int = Field(default=3, ge=1, le=10)
    media: list[dict[str, Any]] = Field(default_factory=list, max_length=MAX_MEDIA)
    customResources: list[dict[str, Any]] = Field(
        default_factory=list, max_length=MAX_RESOURCES
    )
    favorites: list[str] = Field(default_factory=list, max_length=MAX_FAVORITES)
    queue: list[str] = Field(default_factory=list, max_length=MAX_QUEUE)
    resume: dict[str, Any] = Field(default_factory=dict)
    settings: dict[str, Any] = Field(default_factory=dict)
    lastView: str = Field(default="discover", max_length=40)
    updatedAt: int | float | str | None = None

    @field_validator("lastView")
    @classmethod
    def validate_last_view(cls, value: str) -> str:
        allowed = {"discover", "search", "channels", "library", "resources"}
        return value if value in allowed else "discover"


class FleaPitStatePut(BaseModel):
    state: FleaPitState
    baseRevision: int | None = Field(default=None, ge=0)
    reason: str = Field(default="member-sync", min_length=1, max_length=160)

    @field_validator("state")
    @classmethod
    def bound_serialized_state(cls, value: FleaPitState) -> FleaPitState:
        encoded = json.dumps(value.model_dump(mode="json"), separators=(",", ":")).encode(
            "utf-8"
        )
        if len(encoded) > MAX_STATE_BYTES:
            raise ValueError("FleaPit synchronized state exceeds the 2 MB limit.")
        return value


class SnapshotCreate(BaseModel):
    reason: str = Field(default="manual", min_length=1, max_length=160)


@router.get("/status")
async def status_route() -> dict[str, Any]:
    upstream = await fleapit_status()
    return {
        "service": "FleaPit",
        "network": "333 Network",
        "state": str(upstream.get("state") or "backend-ready"),
        "backend": "OHMIC Foundry",
        "purpose": "member-media-library",
        "encryptedPersistence": bool((upstream.get("vault") or {}).get("encryptedAtRest")),
        "mediaBytes": False,
        "mediaMode": "metadata-links-and-library-state",
        "counts": upstream.get("counts") or {},
    }


@router.get("/state")
async def state_get_route(
    member: SovereignMember = Depends(get_current_sovereign_member),
) -> dict[str, Any]:
    return await get_state(member_id=member.id)


@router.put("/state")
async def state_put_route(
    payload: FleaPitStatePut,
    member: SovereignMember = Depends(get_current_sovereign_member),
    _csrf: None = Depends(require_fleapit_csrf),
) -> dict[str, Any]:
    return await put_state(
        member_id=member.id,
        state=payload.state.model_dump(mode="json"),
        base_revision=payload.baseRevision,
        reason=payload.reason,
    )


@router.get("/snapshots")
async def snapshots_list_route(
    member: SovereignMember = Depends(get_current_sovereign_member),
) -> dict[str, Any]:
    return await list_snapshots(member_id=member.id)


@router.post("/snapshots", status_code=status.HTTP_201_CREATED)
async def snapshot_create_route(
    payload: SnapshotCreate,
    member: SovereignMember = Depends(get_current_sovereign_member),
    _csrf: None = Depends(require_fleapit_csrf),
) -> dict[str, Any]:
    return await create_snapshot(member_id=member.id, reason=payload.reason)


@router.post("/snapshots/{snapshot_id}/restore")
async def snapshot_restore_route(
    snapshot_id: str,
    member: SovereignMember = Depends(get_current_sovereign_member),
    _csrf: None = Depends(require_fleapit_csrf),
) -> dict[str, Any]:
    return await restore_snapshot(member_id=member.id, snapshot_id=snapshot_id)
