"""Asynchronous SQLAlchemy engine and session lifecycle."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from dataclasses import asdict, dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

LOGGER = logging.getLogger("network333.database")


@dataclass(frozen=True, slots=True)
class DatabaseHealth:
    ok: bool
    latency_ms: float | None
    status: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_timeout=settings.database_pool_timeout_seconds,
    )


engine = _create_engine()

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_database_session() -> AsyncIterator[AsyncSession]:
    """Yield one request-scoped session with rollback on failure."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def database_health_check(
    timeout_seconds: float | None = None,
) -> DatabaseHealth:
    """Run a bounded SELECT 1 check without exposing connection details."""
    timeout = timeout_seconds or settings.database_health_timeout_seconds
    started = time.perf_counter()

    try:
        async with asyncio.timeout(timeout):
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        return DatabaseHealth(ok=True, latency_ms=latency_ms, status="available")
    except TimeoutError:
        LOGGER.warning("database_health_timeout timeout_seconds=%s", timeout)
        return DatabaseHealth(ok=False, latency_ms=None, status="timeout")
    except Exception:
        LOGGER.exception("database_health_failed")
        return DatabaseHealth(ok=False, latency_ms=None, status="unavailable")


async def dispose_engine() -> None:
    """Release pooled database connections during application shutdown."""
    await engine.dispose()
