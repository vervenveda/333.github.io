"""Append-only administrative and security audit events."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class AuditLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audit_logs"

    actor_user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )
    resource_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )
    outcome: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="success",
        server_default="success",
        index=True,
    )
    request_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )
    ip_address_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    details: Mapped[dict[str, object]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )
