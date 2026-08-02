"""Append audit events within an existing transaction."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog


async def record_audit(
    session: AsyncSession,
    *,
    event_type: str,
    resource_type: str,
    actor_user_id: UUID | None = None,
    resource_id: str | None = None,
    outcome: str = "success",
    request_id: str | None = None,
    ip_address_hash: str | None = None,
    details: dict[str, object] | None = None,
) -> AuditLog:
    event = AuditLog(
        actor_user_id=actor_user_id,
        event_type=event_type,
        resource_type=resource_type,
        resource_id=resource_id,
        outcome=outcome,
        request_id=request_id,
        ip_address_hash=ip_address_hash,
        details=details or {},
    )
    session.add(event)
    await session.flush()
    return event
