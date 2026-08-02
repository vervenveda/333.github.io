"""Initial administrator endpoints for E=Ven Mail review."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_database_session
from app.core.permissions import Role
from app.dependencies.permissions import require_roles
from app.models.user import User
from app.schemas.even_mail import (
    EmailApplicationResponse,
    EmailApplicationReview,
)
from app.services.email_application_service import (
    list_all_applications,
    review_application,
)

router = APIRouter()


@router.get(
    "/even-mail/applications",
    response_model=list[EmailApplicationResponse],
)
async def applications(
    status: str | None = Query(default=None, max_length=32),
    _: User = Depends(
        require_roles(Role.MAIL_ADMIN, Role.ADMINISTRATOR)
    ),
    session: AsyncSession = Depends(get_database_session),
):
    return await list_all_applications(session, status=status)


@router.post(
    "/even-mail/applications/{application_id}/review",
    response_model=EmailApplicationResponse,
)
async def review(
    application_id: UUID,
    payload: EmailApplicationReview,
    request: Request,
    reviewer: User = Depends(
        require_roles(Role.MAIL_ADMIN, Role.ADMINISTRATOR)
    ),
    session: AsyncSession = Depends(get_database_session),
):
    return await review_application(
        session,
        reviewer=reviewer,
        application_id=application_id,
        decision=payload.decision,
        administrator_notes=payload.administrator_notes,
        request_id=getattr(request.state, "request_id", None),
    )
