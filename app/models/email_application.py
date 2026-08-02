"""E=Ven Mail address application model."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import EmailApplicationStatus


class EmailApplication(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "email_applications"

    reference: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    requested_local_part: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    requested_domain: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    requested_address: Mapped[str] = mapped_column(
        String(320),
        nullable=False,
        index=True,
    )
    alternate_contact_email: Mapped[str | None] = mapped_column(
        String(320),
        nullable=True,
    )
    purpose: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=EmailApplicationStatus.SUBMITTED.value,
        server_default=EmailApplicationStatus.SUBMITTED.value,
        index=True,
    )
    applicant_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    administrator_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    reviewed_by_user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="email_applications",
    )
    reviewer = relationship("User", foreign_keys=[reviewed_by_user_id])
