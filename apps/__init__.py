"""SQLAlchemy model package.

Import future model modules here so Alembic can discover their tables.
"""

from app.models.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

__all__ = ["Base", "TimestampMixin", "UUIDPrimaryKeyMixin"]
