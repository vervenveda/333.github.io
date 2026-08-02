"""Existing and provisional 333 member numbers."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import NumberKind, NumberStatus


class NetworkNumber(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "network_numbers"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )
    kind: Mapped[str] = mapped_column(
        String(24),
        nullable=False,
        default=NumberKind.NETWORK.value,
        server_default=NumberKind.NETWORK.value,
    )
    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default=NumberStatus.PROVISIONAL.value,
        server_default=NumberStatus.PROVISIONAL.value,
        index=True,
    )
    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )
    verification_method: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True,
    )
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user = relationship("User", back_populates="network_numbers")
