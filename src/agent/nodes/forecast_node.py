"""
Forecast Node
Ingests FortyGuard 2-meter ambient air temperature, solar irradiance, 12-hour forward
forecast, and continuous persistence/exceedance metrics.
"""

from __future__ import annotations

import time
from typing import Any, Dict
from src.agent.state import ThermalSentinelState
from src.api.fortyguard_client import AsyncFortyGuardClient


async def forecast_node(state: ThermalSentinelState) -> Dict[str, Any]:
    """
    Fetches the 12-hour forward microclimate forecast and persistence layers.
    """
    loc = state.get("location", {"lat": 33.4484, "lon": -112.0740})
    client = AsyncFortyGuardClient()

    forecast = await client.get_12h_forecast(
        latitude=loc.get("lat", 33.4484),
        longitude=loc.get("lon", -112.0740),
    )
    persistence = await client.get_persistence_and_exceedance(
        latitude=loc.get("lat", 33.4484),
        longitude=loc.get("lon", -112.0740),
        threshold_c=40.0,
    )

    audit_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()),
        "node": "forecast_node",
        "message": f"Ingested 12h forecast for {state.get('target_city', 'Phoenix, AZ')} (Peak 2m ambient: {forecast[7]['fortyguard_2m_ambient_c']}°C, Persistence: {persistence.get('persistence_hours_p40')}h > 40°C)",
    }

    audit_trail = list(state.get("audit_trail", []))
    audit_trail.append(audit_entry)

    return {
        "fortyguard_forecast": forecast,
        "persistence_metrics": persistence,
        "audit_trail": audit_trail,
        "current_node": "forecast_node",
    }
