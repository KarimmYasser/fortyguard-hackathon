"""Small process-local concurrency and pacing governor for public providers."""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager


class AsyncRateLimiter:
    """Bound concurrency and minimum spacing without pretending to be a quota."""

    def __init__(self, *, max_concurrency: int = 2, min_interval_s: float = 0.1) -> None:
        if max_concurrency < 1 or min_interval_s < 0:
            raise ValueError("invalid rate limiter configuration")
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._lock = asyncio.Lock()
        self._last_request = 0.0
        self.min_interval_s = min_interval_s

    @asynccontextmanager
    async def slot(self):
        async with self._semaphore:
            async with self._lock:
                remaining = self.min_interval_s - (time.monotonic() - self._last_request)
                if remaining > 0:
                    await asyncio.sleep(remaining)
                self._last_request = time.monotonic()
            yield


_LIMITERS: dict[str, AsyncRateLimiter] = {}


def provider_limiter(provider: str, *, max_concurrency: int = 2, min_interval_s: float = 0.1) -> AsyncRateLimiter:
    limiter = _LIMITERS.get(provider)
    if limiter is None:
        limiter = _LIMITERS[provider] = AsyncRateLimiter(
            max_concurrency=max_concurrency, min_interval_s=min_interval_s
        )
    return limiter
