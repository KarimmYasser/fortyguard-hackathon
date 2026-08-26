"""Shared bounded retry policy for best-effort public evidence services."""

from __future__ import annotations

import asyncio
import random
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from typing import Mapping

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def retry_delay(attempt: int, headers: Mapping[str, str] | None = None, *, jitter: bool = True) -> float:
    """Return a bounded delay, honoring numeric or HTTP-date Retry-After."""
    raw = (headers or {}).get("retry-after") or (headers or {}).get("Retry-After")
    delay: float | None = None
    if raw:
        try:
            delay = float(raw)
        except ValueError:
            try:
                parsed = parsedate_to_datetime(raw)
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                delay = max(0.0, (parsed - datetime.now(timezone.utc)).total_seconds())
            except (TypeError, ValueError, OverflowError):
                delay = None
    if delay is None:
        delay = 0.25 * (2 ** max(0, attempt))
    delay = min(max(delay, 0.0), 30.0)
    return delay + (random.uniform(0, min(0.25, delay * 0.1)) if jitter and delay else 0.0)


async def sleep_before_retry(attempt: int, headers: Mapping[str, str] | None = None) -> None:
    await asyncio.sleep(retry_delay(attempt, headers))
