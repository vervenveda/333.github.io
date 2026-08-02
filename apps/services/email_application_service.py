"""E=Ven Mail application submission and administrative review."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictError, NotFoundError, ValidationServiceError
from app.models.email_application import EmailApplication
from app.models.enums import EmailApplicationStatus
from app.models.user import User
from app.schemas.even_mail import EmailApplicationCreate, ReviewDecision
from app.services.audit_service import record_audit

ACTIVE_STATUSES = {
    EmailApplicationStatus.SUBMITTED.value,
    EmailApplicationStatus.UNDER_REVIEW.value,
    EmailApplicationStatus.APPROVED.value,
}


def utc_now() -> datetime:
    return datetime.now(UTC)


def make_reference() -> str:
    date = utc_now().strftime("%Y%m%d")
    return f"EVEN-{date}-{secrets.token_hex(4).upper()}"


async def submit_application(
    session: AsyncSession,
    *,
    user: User,
    payload: EmailApplicationCreate,
    request_id: str | None = None,
) -> EmailApplication:
    domain = payload.requested_domain.casefold()
    allowed = {item.casefold() for item in settings.even_mail_allowed_domains}
    if domain not in allowed:
        raise ValidationServiceError(
            "That E=Ven Mail domain is not available for applications."
        )

    address = f"{payload.requested_local_part}@{domain}"
    existing = await session.scalar(
        select(EmailApplication.id).where(
            EmailApplication.requested_address == address,
            EmailApplication.status.in_(ACTIVE_STATUSES),
        )
    )
    if existing:
        raise ConflictError(
            "That requested E=Ven address already has an active application."
        )

    application = EmailApplication(
        reference=make_reference(),
        user_id=user.id,
        requested_local_part=payload.requested_local_part,
        requested_domain=domain,
        requested_address=address,
        alternate_contact_email=(
            str(payload.alternate_contact_email)
            if payload.alternate_contact_email
            else None
        ),
        purpose=payload.purpose,
        applicant_notes=payload.applicant_notes,
        status=EmailApplicationStatus.SUBMITTED.value,
        submitted_at=utc_now(),
    )
    session.add(application)
    await session.flush()

    await record_audit(
        session,
        actor_user_id=user.id,
        event_type="even_mail.application_submitted",
        resource_type="email_application",
        resource_id=str(application.id),
        request_id=request_id,
        details={
            "reference": application.reference,
            "requested_address": application.requested_address,
        },
    )
    await session.commit()
    await session.refresh(application)
    return application


async def list_user_applications(
    session: AsyncSession,
    *,
    user_id,
) -> list[EmailApplication]:
    result = await session.scalars(
        select(EmailApplication)
        .where(EmailApplication.user_id == user_id)
        .order_by(EmailApplication.created_at.desc())
    )
    return list(result.all())


async def withdraw_application(
    session: AsyncSession,
    *,
    user: User,
    application_id,
    request_id: str | None = None,
) -> EmailApplication:
    application = await session.scalar(
        select(EmailApplication).where(
            EmailApplication.id == application_id,
            EmailApplication.user_id == user.id,
        )
    )
    if not application:
        raise NotFoundError("The email application was not found.")
    if application.status == EmailApplicationStatus.APPROVED.value:
        raise ConflictError("An approved application cannot be withdrawn here.")
    if application.status == EmailApplicationStatus.WITHDRAWN.value:
        return application

    application.status = EmailApplicationStatus.WITHDRAWN.value
    await record_audit(
        session,
        actor_user_id=user.id,
        event_type="even_mail.application_withdrawn",
        resource_type="email_application",
        resource_id=str(application.id),
        request_id=request_id,
        details={"reference": application.reference},
    )
    await session.commit()
    await session.refresh(application)
    return application


async def list_all_applications(
    session: AsyncSession,
    *,
    status: str | None = None,
) -> list[EmailApplication]:
    query = select(EmailApplication).order_by(
        EmailApplication.created_at.desc()
    )
    if status:
        query = query.where(EmailApplication.status == status)
    result = await session.scalars(query)
    return list(result.all())


async def review_application(
    session: AsyncSession,
    *,
    reviewer: User,
    application_id,
    decision: ReviewDecision,
    administrator_notes: str | None,
    request_id: str | None = None,
) -> EmailApplication:
    application = await session.get(EmailApplication, application_id)
    if not application:
        raise NotFoundError("The email application was not found.")
    if application.status == EmailApplicationStatus.WITHDRAWN.value:
        raise ConflictError("A withdrawn application cannot be reviewed.")

    if decision is ReviewDecision.APPROVE:
        application.status = EmailApplicationStatus.APPROVED.value
    elif decision is ReviewDecision.REJECT:
        application.status = EmailApplicationStatus.REJECTED.value
    else:
        application.status = EmailApplicationStatus.UNDER_REVIEW.value

    application.administrator_notes = administrator_notes
    application.reviewed_by_user_id = reviewer.id
    application.reviewed_at = utc_now()

    await record_audit(
        session,
        actor_user_id=reviewer.id,
        event_type="even_mail.application_reviewed",
        resource_type="email_application",
        resource_id=str(application.id),
        request_id=request_id,
        details={
            "reference": application.reference,
            "decision": decision.value,
            "status": application.status,
        },
    )
    await session.commit()
    await session.refresh(application)
    return application
