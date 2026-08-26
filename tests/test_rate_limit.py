import pytest

from src.api.rate_limit import AsyncRateLimiter
from src.api.retry import retry_delay


def test_retry_after_is_honored_and_bounded():
    assert retry_delay(0, {"Retry-After": "4"}, jitter=False) == 4
    assert retry_delay(20, {}, jitter=False) == 30


@pytest.mark.asyncio
async def test_rate_limiter_context_is_usable():
    limiter = AsyncRateLimiter(max_concurrency=1, min_interval_s=0)
    async with limiter.slot():
        assert True
