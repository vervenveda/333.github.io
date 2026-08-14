"""Sovereign HOLLO enrollment, profile, and 333 phone-number endpoints."""

from __future__ import annotations
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.dependencies.sovereign_authentication import SovereignMember, get_current_sovereign_member
from app.schemas.hollo import EnrollmentRequest, EnrollmentResponse, NetworkNumberResponse, NumberRequest
from app.schemas.profile import ProfileResponse
from app.services.ohmic_identity_service import add_number, enroll_identity, get_profile, list_numbers

router = APIRouter()

def _dt(value: object) -> datetime | None:
    if value in {None, ""}: return None
    text = str(value).strip()
    if text.endswith("Z"): text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)

def _profile(p: dict[str, object]) -> ProfileResponse:
    return ProfileResponse(id=UUID(str(p["id"])), user_id=UUID(str(p["userId"])), display_name=str(p["displayName"]), handle=str(p["handle"]), bio=p.get("bio"), avatar_url=p.get("avatarUrl"), visibility=str(p.get("visibility") or "members"), created_at=_dt(p["createdAt"]), updated_at=_dt(p["updatedAt"]))

def _number(n: dict[str, object]) -> NetworkNumberResponse:
    return NetworkNumberResponse(id=UUID(str(n["id"])), user_id=UUID(str(n["userId"])), number=str(n["number"]), kind=str(n["kind"]), status=str(n["status"]), is_primary=bool(n["isPrimary"]), verification_method=n.get("verificationMethod"), verified_at=_dt(n.get("verifiedAt")), created_at=_dt(n["createdAt"]), updated_at=_dt(n["updatedAt"]))

def _notice(number: NetworkNumberResponse) -> str:
    return "The 333 phone number is provisional until the sovereign phone system confirms final availability." if number.kind == "network" else "The existing phone number remains pending until verification succeeds."

@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll(payload: EnrollmentRequest, member: SovereignMember = Depends(get_current_sovereign_member)) -> EnrollmentResponse:
    result = await enroll_identity(member_id=member.id, profile=payload.profile.model_dump(mode="json"), number=payload.number.model_dump(mode="json"))
    profile = _profile(dict(result["profile"])); number = _number(dict(result["number"]))
    return EnrollmentResponse(profile=profile, number=number, notice=_notice(number))

@router.get("/profile", response_model=ProfileResponse)
async def profile(member: SovereignMember = Depends(get_current_sovereign_member)) -> ProfileResponse:
    return _profile(await get_profile(member_id=member.id))

@router.get("/numbers", response_model=list[NetworkNumberResponse])
async def numbers(member: SovereignMember = Depends(get_current_sovereign_member)) -> list[NetworkNumberResponse]:
    return [_number(item) for item in await list_numbers(member_id=member.id)]

@router.post("/numbers", response_model=NetworkNumberResponse, status_code=status.HTTP_201_CREATED)
async def add_phone_number(payload: NumberRequest, member: SovereignMember = Depends(get_current_sovereign_member)) -> NetworkNumberResponse:
    return _number(await add_number(member_id=member.id, number=payload.model_dump(mode="json")))
