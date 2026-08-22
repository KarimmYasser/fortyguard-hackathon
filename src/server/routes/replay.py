"""
Historical Replay Router
Serves the Phoenix July 2023 heatwave benchmark replay dataset for baseline vs. mitigated comparison.
"""

from __future__ import annotations

import logging

from typing import Any, Dict
from fastapi import APIRouter, Response
from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine

from src.db.database import db_manager
from src.db.models import SubstationTelemetryRecord, MultiDayHeatwaveRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/replay", tags=["Historical Replay"])

_REPLAY_ENGINE = PhoenixHeatwaveReplayEngine()


@router.get("/phoenix-2023")
async def get_phoenix_2023_replay(response: Response) -> Dict[str, Any]:
    """
    Returns complete 12-hour synchronized replay telemetry comparing
    Baseline Controller vs. Thermal Sentinel Grid during Phoenix July 2023, logging to database.
    """
    # The replay is a deterministic recomputation of a fixed historical
    # scenario, so every visitor was paying a multi-second cold start for an
    # identical payload. Let the Vercel edge serve it and revalidate in the
    # background; the browser still revalidates so a redeploy is picked up.
    response.headers["Cache-Control"] = (
        "public, max-age=0, s-maxage=600, stale-while-revalidate=86400"
    )

    data = _REPLAY_ENGINE.generate_replay_dataset()
    # The engine is synchronous, so it buffers CBF certificates rather than
    # scheduling background writes that a frozen lambda would cancel.
    await _REPLAY_ENGINE.safety_gate.persist_pending_certificates()

    try:
        steps = data.get("timeline_steps", [])
        for s in steps:
            rec = SubstationTelemetryRecord(
                asset_id="SUB-PHX-DOWNTOWN-04",
                hour_step=s.get("hour_index", 0),
                ambient_c=s.get("fortyguard_2m_ambient_c", 43.1),
                top_oil_c=s.get("mitigated_top_oil_c", 98.0),
                hot_spot_c=s.get("mitigated_hot_spot_c", 136.8),
                aging_factor=s.get("mitigated_aging_factor_v", 1.8),
                load_ratio=s.get("mitigated_load_k", 0.88),
                bess_dispatch_mw=4.5,
                is_mitigated=True,
            )
            await db_manager.log_substation_telemetry(rec)
    except Exception as exc:
        logger.warning("Failed to persist substation telemetry: %s", exc, exc_info=True)

    return data

