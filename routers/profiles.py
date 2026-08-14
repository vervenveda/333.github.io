"""Sovereign current-member HOLLO profile endpoints backed by OHMIC."""

from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends
from app.dependencies.sovereign_authentication import SovereignMember, get_current_sovereign_member
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.ohmic_identity_service import get_profile, update_profile

router = APIRouter()

def _dt(value: object) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"): text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)

def _response(profile: dict[str, object]) -> ProfileResponse:
    return ProfileResponse(id=UUID(str(profile["id"])), user_id=UUID(str(profile["userId"])), display_name=str(profile["displayName"]), handle=str(profile["handle"]), bio=profile.get("bio"), avatar_url=profile.get("avatarUrl"), visibility=str(profile.get("visibility") or "members"), created_at=_dt(profile["createdAt"]), updated_at=_dt(profile["updatedAt"]))

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(member: SovereignMember = Depends(get_current_sovereign_member)) -> ProfileResponse:
    return _response(await get_profile(member_id=member.id))

@router.patch("/me", response_model=ProfileResponse)
async def patch_my_profile(payload: ProfileUpdate, member: SovereignMember = Depends(get_current_sovereign_member)) -> ProfileResponse:
    return _response(await update_profile(member_id=member.id, changes=payload.model_dump(exclude_unset=True)))
