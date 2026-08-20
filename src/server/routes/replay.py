"""
Historical Replay Router
Serves the Phoenix July 2023 heatwave benchmark replay dataset for baseline vs. mitigated comparison.
"""

from __future__ import annotations

from typing import Any, Dict
from fastapi import APIRouter
from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine

router = APIRouter(prefix="/replay", tags=["Historical Replay"])

_REPLAY_ENGINE = PhoenixHeatwaveReplayEngine()


@router.get("/phoenix-2023")
async def get_phoenix_2023_replay() -> Dict[str, Any]:
    """
    Returns complete 12-hour synchronized replay telemetry comparing
    Baseline Controller vs. Thermal Sentinel Grid during Phoenix July 2023.
    """
    return _REPLAY_ENGINE.generate_replay_dataset()
