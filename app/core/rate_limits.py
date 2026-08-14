"""Process-local fixed-window rate limiting for the sovereign 333 runtime.

Rate-limit counters are intentionally ephemeral operational state, not member
records. Persistent identity and session authority remain in OHMIC Foundry.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass

from app.core.exceptions import RateLimitError


@dataclass(frozen=True, slots=True)
class RateLimitResult:
    allowed: bool
    remaining: int
    retry_after: int


@dataclass(slots=True)
class _Bucket:
    started_at: float
    count: int


class RateLimiter:
    """Dependency-free in-process fixed-window limiter."""

    def __init__(self) -> None:
        self._buckets: dict[str, _Bucket] = {}
        self._lock = asyncio.Lock()

    async def check(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        fail_closed: bool | None = None,
    ) -> RateLimitResult:
        del fail_closed  # retained for call compatibility with the previous API
        if limit <= 0 or window_seconds <= 0:
            return RateLimitResult(allowed=True, remaining=max(limit, 0), retry_after=0)

        current = time.monotonic()
        async with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None or current - bucket.started_at >= window_seconds:
                bucket = _Bucket(started_at=current, count=1)
                self._buckets[key] = bucket
            else:
                bucket.count += 1

            elapsed = current - bucket.started_at
            retry_after = max(int(window_seconds - elapsed), 1)
            remaining = max(limit - bucket.count, 0)
            allowed = bucket.count <= limit

            # Opportunistic cleanup prevents unbounded growth without a worker.
            if len(self._buckets) > 10000:
                cutoff = current - max(window_seconds * 2, 120)
                self._buckets = {
                    item_key: item
                    for item_key, item in self._buckets.items()
                    if item.started_at >= cutoff
                }

        return RateLimitResult(
            allowed=allowed,
            remaining=remaining,
            retry_after=retry_after,
        )

    async def enforce(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        fail_closed: bool | None = None,
    ) -> RateLimitResult:
        result = await self.check(
            key=key,
            limit=limit,
            window_seconds=window_seconds,
            fail_closed=fail_closed,
        )
        if not result.allowed:
            raise RateLimitError(
                "Too many requests. Try again later.",
                details={"retry_after": result.retry_after},
            )
        return result

    async def close(self) -> None:
        async with self._lock:
            self._buckets.clear()


rate_limiter = RateLimiter()
