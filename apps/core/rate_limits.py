"""Redis-backed fixed-window rate limiting for sensitive endpoints."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.core.config import settings
from app.core.exceptions import RateLimitError

LOGGER = logging.getLogger("network333.rate_limits")


@dataclass(frozen=True, slots=True)
class RateLimitResult:
    allowed: bool
    remaining: int
    retry_after: int


class RateLimiter:
    """Small fixed-window limiter using atomic Redis increments."""

    def __init__(self, redis_url: str | None = None):
        self._redis = Redis.from_url(
            redis_url or settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def check(
        self,
        *,
        key: str,
        limit: int,
        window_seconds: int,
        fail_closed: bool | None = None,
    ) -> RateLimitResult:
        close_on_error = (
            settings.rate_limit_fail_closed
            if fail_closed is None
            else fail_closed
        )
        redis_key = f"network333:rate:{key}"

        try:
            value = await self._redis.incr(redis_key)
            if value == 1:
                await self._redis.expire(redis_key, window_seconds)
            ttl = await self._redis.ttl(redis_key)
        except RedisError as exc:
            LOGGER.exception("rate_limit_redis_failed")
            if close_on_error:
                raise RateLimitError(
                    "This action is temporarily unavailable."
                ) from exc
            return RateLimitResult(
                allowed=True,
                remaining=limit,
                retry_after=0,
            )

        remaining = max(limit - int(value), 0)
        retry_after = max(int(ttl), 1)
        return RateLimitResult(
            allowed=int(value) <= limit,
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
        await self._redis.aclose()


rate_limiter = RateLimiter()
