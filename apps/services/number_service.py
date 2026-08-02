"""Reservation of provisional 333 numbers and existing-number records."""

from __future__ import annotations

import re
import secrets

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictError, ValidationServiceError
from app.models.enums import NumberKind, NumberStatus
from app.models.network_number import NetworkNumber
from app.models.user import User
from app.schemas.hollo import NumberChoice, NumberRequest
from app.services.audit_service import record_audit

PROTECTED_SERVICE_ROUTES = frozenset(
    {
        "3331117777",
        "3332227777",
        "3333337777",
        "3334447777",
    }
)


def normalize_number(value: str) -> str:
    return re.sub(r"\D", "", value)


def validate_existing_number(number: str) -> str:
    normalized = normalize_number(number)
    if not 7 <= len(normalized) <= 15:
        raise ValidationServiceError(
            "Existing numbers must contain between 7 and 15 digits."
        )
    if normalized in PROTECTED_SERVICE_ROUTES:
        raise ValidationServiceError(
            "That number is reserved for a 333 Network service."
        )
    return normalized


async def _make_primary(
    session: AsyncSession,
    *,
    user_id,
) -> None:
    await session.execute(
        update(NetworkNumber)
        .where(NetworkNumber.user_id == user_id)
        .values(is_primary=False)
    )


async def reserve_provisional_number(
    session: AsyncSession,
    *,
    user: User,
    make_primary: bool = True,
    request_id: str | None = None,
) -> NetworkNumber:
    prefix = settings.network_number_prefix
    suffix_length = settings.network_number_total_digits - len(prefix)
    if suffix_length < 4:
        raise RuntimeError("NETWORK_NUMBER_TOTAL_DIGITS is too small.")

    if make_primary:
        await _make_primary(session, user_id=user.id)

    for _ in range(75):
        suffix = "".join(
            str(secrets.randbelow(10)) for _ in range(suffix_length)
        )
        number = f"{prefix}{suffix}"
        if number in PROTECTED_SERVICE_ROUTES:
            continue

        exists = await session.scalar(
            select(NetworkNumber.id).where(NetworkNumber.number == number)
        )
        if exists:
            continue

        record = NetworkNumber(
            user_id=user.id,
            number=number,
            kind=NumberKind.NETWORK.value,
            status=NumberStatus.PROVISIONAL.value,
            is_primary=make_primary,
        )
        session.add(record)
        try:
            await session.flush()
            await record_audit(
                session,
                actor_user_id=user.id,
                event_type="network_number.provisionally_reserved",
                resource_type="network_number",
                resource_id=str(record.id),
                request_id=request_id,
                details={"number_suffix": number[-4:]},
            )
            await session.commit()
            await session.refresh(record)
            return record
        except IntegrityError:
            await session.rollback()
            continue

    raise ConflictError("A provisional 333 number could not be reserved.")


async def register_existing_number(
    session: AsyncSession,
    *,
    user: User,
    number: str,
    make_primary: bool = True,
    request_id: str | None = None,
) -> NetworkNumber:
    normalized = validate_existing_number(number)
    exists = await session.scalar(
        select(NetworkNumber.id).where(NetworkNumber.number == normalized)
    )
    if exists:
        raise ConflictError("That number is already connected to an account.")

    if make_primary:
        await _make_primary(session, user_id=user.id)

    record = NetworkNumber(
        user_id=user.id,
        number=normalized,
        kind=NumberKind.EXISTING.value,
        status=NumberStatus.PENDING_VERIFICATION.value,
        is_primary=make_primary,
        verification_method="pending",
    )
    session.add(record)

    try:
        await session.flush()
        await record_audit(
            session,
            actor_user_id=user.id,
            event_type="existing_number.recorded",
            resource_type="network_number",
            resource_id=str(record.id),
            request_id=request_id,
            details={"number_suffix": normalized[-4:]},
        )
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ConflictError(
            "That number is already connected to an account."
        ) from exc

    await session.refresh(record)
    return record


async def create_number_from_request(
    session: AsyncSession,
    *,
    user: User,
    payload: NumberRequest,
    request_id: str | None = None,
) -> NetworkNumber:
    if payload.choice is NumberChoice.EXISTING:
        return await register_existing_number(
            session,
            user=user,
            number=payload.existing_number or "",
            make_primary=payload.make_primary,
            request_id=request_id,
        )
    return await reserve_provisional_number(
        session,
        user=user,
        make_primary=payload.make_primary,
        request_id=request_id,
    )


async def list_numbers(
    session: AsyncSession,
    *,
    user_id,
) -> list[NetworkNumber]:
    result = await session.scalars(
        select(NetworkNumber)
        .where(NetworkNumber.user_id == user_id)
        .order_by(NetworkNumber.is_primary.desc(), NetworkNumber.created_at)
    )
    return list(result.all())
