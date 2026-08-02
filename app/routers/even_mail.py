"""Member E=Ven Mail application endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_database_session
from app.core.rate_limits import rate_limiter
from app.dependencies.authentication import get_current_user
from app.models.user import User
from app.schemas.even_mail import (
    EmailApplicationCreate,
    EmailApplicationResponse,
)
from app.services.email_application_service import (
    list_user_applications,
    submit_application,
    withdraw_application,
)

router = APIRouter()


@router.post(
    "/applications",
    response_model=EmailApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    payload: EmailApplicationCreate,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    await rate_limiter.enforce(
        key=f"even-application:{user.id}",
        limit=settings.email_application_rate_limit,
        window_seconds=86400,
    )
    return await submit_application(
        session,
        user=user,
        payload=payload,
        request_id=getattr(request.state, "request_id", None),
    )


@router.get(
    "/applications/me",
    response_model=list[EmailApplicationResponse],
)
async def my_applications(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await list_user_applications(session, user_id=user.id)


@router.post(
    "/applications/{application_id}/withdraw",
    response_model=EmailApplicationResponse,
)
async def withdraw(
    application_id: UUID,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_database_session),
):
    return await withdraw_application(
        session,
        user=user,
        application_id=application_id,
        request_id=getattr(request.state, "request_id", None),
    )
