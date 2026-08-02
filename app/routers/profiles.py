"""Current member profile endpoints."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.dependencies.authentication import get_current_user
from app.models.user import User
from app.schemas.profile import ProfileResponse, ProfileUpdate
from app.services.identity_service import get_profile_for_user, update_profile

router = APIRouter()


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await get_profile_for_user(session, user_id=user.id)


@router.patch("/me", response_model=ProfileResponse)
async def patch_my_profile(
    payload: ProfileUpdate,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    profile = await get_profile_for_user(session, user_id=user.id)
    return await update_profile(
        session,
        profile=profile,
        user=user,
        payload=payload,
        request_id=getattr(request.state, "request_id", None),
    )
