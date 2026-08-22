"""
Historical Replay Router
Serves the Phoenix July 2023 heatwave benchmark replay dataset for baseline vs. mitigated comparison.
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Response

from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine

router = APIRouter(prefix="/replay", tags=["Historical Replay"])

_REPLAY_ENGINE = PhoenixHeatwaveReplayEngine()


@router.get("/phoenix-2023")
async def get_phoenix_2023_replay(response: Response) -> Dict[str, Any]:
    """
    Returns complete 12-hour synchronized replay telemetry comparing
    Baseline Controller vs. Thermal Sentinel Grid during Phoenix July 2023.

    This GET is deliberately read-only. The replay is a checked-in deterministic
    fixture, so persisting the same 12 telemetry rows and a new safety certificate
    for every page load only creates duplicates and unnecessary database traffic.
    """
    # The replay is a deterministic recomputation of a fixed historical
    # scenario, so every visitor was paying a multi-second cold start for an
    # identical payload. Let the Vercel edge serve it and revalidate in the
    # background; the browser still revalidates so a redeploy is picked up.
    response.headers["Cache-Control"] = (
        "public, max-age=0, s-maxage=600, stale-while-revalidate=86400"
    )

    data = _REPLAY_ENGINE.generate_replay_dataset()
    # Evaluation buffers a certificate for mutation-oriented callers. A replay
    # read must neither write it nor leave it queued on the singleton engine.
    _REPLAY_ENGINE.safety_gate.pending_certificates.clear()
    return data

