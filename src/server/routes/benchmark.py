"""
FastAPI Routes for IEEE C57.91 Annex G Benchmarking & 72-Hour Compounding Replay
"""

from __future__ import annotations

from typing import Dict, Any
from fastapi import APIRouter

from src.physics.ieee_annex_g_benchmark import IEEEAnnexGBenchmarkEngine
from src.physics.multi_day_heatwave import MultiDayHeatwaveEngine

router = APIRouter(tags=["Academic Standards & 72h Compounding"])


@router.get("/api/v1/benchmark/ieee-annex-g")
async def get_ieee_annex_g_validation() -> Dict[str, Any]:
    """
    Executes the official IEEE Std C57.91-2011 Annex G reference benchmark test suite.
    Demonstrates zero deviation from the published IEEE standard numerical tables.
    """
    engine = IEEEAnnexGBenchmarkEngine()
    return engine.run_all_benchmarks()


@router.get("/api/v1/replay/72h-compounding")
async def get_72h_compounding_replay() -> Dict[str, Any]:
    """
    Returns the continuous 72-hour (3-day) rolling heatwave simulation (July 24-26, 2023)
    showing compounding soil moisture depletion, surging rho_soil, and multi-day Arrhenius degradation.
    """
    engine = MultiDayHeatwaveEngine()
    result = engine.run_72h_simulation()
    return result.model_dump()
