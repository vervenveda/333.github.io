"""HOLLO enrollment, profile, and member-number endpoints."""

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.core.exceptions import ConflictError
from app.dependencies.authentication import get_current_user
from app.models.user import User
from app.schemas.hollo import (
    EnrollmentRequest,
    EnrollmentResponse,
    NetworkNumberResponse,
    NumberRequest,
)
from app.schemas.profile import ProfileResponse
from app.services.identity_service import create_profile, get_profile_for_user
from app.services.number_service import (
    create_number_from_request,
    list_numbers,
)

router = APIRouter()


@router.post(
    "/enroll",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enroll(
    payload: EnrollmentRequest,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
) -> EnrollmentResponse:
    # Profile and number are independent service commits in this first release.
    # If number creation fails, the profile remains recoverable and enrollment
    # can continue through POST /numbers.
    try:
        profile = await get_profile_for_user(session, user_id=user.id)
        raise ConflictError("This account is already enrolled in HOLLO.")
    except Exception as exc:
        if isinstance(exc, ConflictError):
            raise
        profile = await create_profile(
            session,
            user=user,
            payload=payload.profile,
            request_id=getattr(request.state, "request_id", None),
        )

    number = await create_number_from_request(
        session,
        user=user,
        payload=payload.number,
        request_id=getattr(request.state, "request_id", None),
    )

    notice = (
        "The 333 number is provisional until production identity services "
        "confirm global availability."
        if number.kind == "network"
        else "The existing number remains pending until verification succeeds."
    )
    return EnrollmentResponse(
        profile=ProfileResponse.model_validate(profile),
        number=NetworkNumberResponse.model_validate(number),
        notice=notice,
    )


@router.get("/profile", response_model=ProfileResponse)
async def profile(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await get_profile_for_user(session, user_id=user.id)


@router.get("/numbers", response_model=list[NetworkNumberResponse])
async def numbers(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await list_numbers(session, user_id=user.id)


@router.post(
    "/numbers",
    response_model=NetworkNumberResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_number(
    payload: NumberRequest,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await create_number_from_request(
        session,
        user=user,
        payload=payload,
        request_id=getattr(request.state, "request_id", None),
    )
