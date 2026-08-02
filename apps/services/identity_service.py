"""Profile creation and update services."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.profile import Profile
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.services.audit_service import record_audit


async def get_profile_for_user(
    session: AsyncSession,
    *,
    user_id,
) -> Profile:
    profile = await session.scalar(
        select(Profile).where(Profile.user_id == user_id)
    )
    if not profile:
        raise NotFoundError("No HOLLO profile exists for this account.")
    return profile


async def create_profile(
    session: AsyncSession,
    *,
    user: User,
    payload: ProfileCreate,
    request_id: str | None = None,
) -> Profile:
    existing = await session.scalar(
        select(Profile).where(Profile.user_id == user.id)
    )
    if existing:
        raise ConflictError("This account already has a HOLLO profile.")

    handle_owner = await session.scalar(
        select(Profile.id).where(Profile.handle == payload.handle)
    )
    if handle_owner:
        raise ConflictError("That HOLLO handle is already reserved.")

    profile = Profile(
        user_id=user.id,
        display_name=payload.display_name,
        handle=payload.handle,
        bio=payload.bio,
        avatar_url=payload.avatar_url,
        visibility=payload.visibility.value,
    )
    session.add(profile)

    try:
        await session.flush()
        await record_audit(
            session,
            actor_user_id=user.id,
            event_type="profile.created",
            resource_type="profile",
            resource_id=str(profile.id),
            request_id=request_id,
            details={"handle": profile.handle},
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("That HOLLO handle is already reserved.") from exc

    await session.refresh(profile)
    return profile


async def update_profile(
    session: AsyncSession,
    *,
    profile: Profile,
    user: User,
    payload: ProfileUpdate,
    request_id: str | None = None,
) -> Profile:
    changes = payload.model_dump(exclude_unset=True)

    if "handle" in changes and changes["handle"] != profile.handle:
        owner = await session.scalar(
            select(Profile.id).where(Profile.handle == changes["handle"])
        )
        if owner:
            raise ConflictError("That HOLLO handle is already reserved.")

    if "visibility" in changes and changes["visibility"] is not None:
        changes["visibility"] = changes["visibility"].value

    for field, value in changes.items():
        setattr(profile, field, value)

    try:
        await record_audit(
            session,
            actor_user_id=user.id,
            event_type="profile.updated",
            resource_type="profile",
            resource_id=str(profile.id),
            request_id=request_id,
            details={"fields": sorted(changes)},
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError("That HOLLO handle is already reserved.") from exc

    await session.refresh(profile)
    return profile
