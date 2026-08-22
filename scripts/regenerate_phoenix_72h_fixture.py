#!/usr/bin/env python3
"""Capture three complete Phoenix days from FortyGuard for the 72h replay.

The former 72h boundary forcing was a hand-authored sinusoid built from retired
airport and heat-trap constants. This script replaces it with a frozen,
reproducible capture of 24 hourly `tcm` measurements for each of 2023-07-24,
2023-07-25 and 2023-07-26.

Temperature statistics are measured by FortyGuard. Solar irradiance is derived
by AsyncFortyGuardClient from the day's live env_params GHI/cloud observations
and solar geometry. Transformer loading remains a grid-side model because
FortyGuard exposes no SCADA.

    python3 scripts/regenerate_phoenix_72h_fixture.py

Requires FORTYGUARD_API_KEY. Cold capture submits 72 tcm jobs plus three
`env_params` jobs; durable api_call_cache makes subsequent regeneration free.
The output is not touched unless all 72 hours validate.
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

FIXTURE = ROOT / "src" / "api" / "fixtures" / "phoenix_heatwave_2023_72h.json"
LAT, LON = 33.4484, -112.0740
DATES = ("2023-07-24", "2023-07-25", "2023-07-26")
HOURS = list(range(24))


async def main() -> int:
    from src.api.fortyguard_client import AsyncFortyGuardClient

    client = AsyncFortyGuardClient()
    if client.mock_mode:
        print("ERROR: mock mode is active; refusing to label fixture data as live.")
        return 1

    captured = []
    for day_number, analysis_date in enumerate(DATES, start=1):
        print(f"Fetching {analysis_date}, hours 00-23 ...", flush=True)
        profile = await client.get_hourly_profile(
            latitude=LAT,
            longitude=LON,
            analysis_date=analysis_date,
            hours=HOURS,
        )

        got_hours = [int(row["timestamp"][11:13]) for row in profile]
        if len(profile) != 24 or got_hours != HOURS:
            print(f"ERROR: {analysis_date} returned {len(profile)} rows / hours {got_hours}; fixture unchanged.")
            return 1
        if any(not str(row.get("data_source", "")).startswith("fortyguard_live") for row in profile):
            print(f"ERROR: {analysis_date} contains non-live rows; fixture unchanged.")
            return 1

        for row, hour in zip(profile, HOURS):
            captured.append(
                {
                    "global_hour": (day_number - 1) * 24 + hour,
                    "day_index": day_number,
                    "date": analysis_date,
                    "hour_of_day": hour,
                    "time_label": f"{hour:02d}:00",
                    "fortyguard_2m_ambient_c": row["fortyguard_2m_ambient_c"],
                    "coolest_tile_2m_c": row["coolest_tile_2m_c"],
                    "tile_peak_2m_c": row["tile_peak_2m_c"],
                    "intra_aoi_spread_c": row["intra_aoi_spread_c"],
                    "relative_humidity_pct": row["relative_humidity_pct"],
                    "wet_bulb_temp_c": row["wet_bulb_temp_c"],
                    "cloud_cover_pct": row["cloud_cover_pct"],
                    "solar_irradiance_w_m2": row["solar_irradiance_w_m2"],
                    "data_source": row["data_source"],
                }
            )
        print(
            f"  peak={max(r['fortyguard_2m_ambient_c'] for r in profile):.2f} C, "
            f"minimum={min(r['fortyguard_2m_ambient_c'] for r in profile):.2f} C",
            flush=True,
        )

    assert len(captured) == 72
    payload = {
        "scenario_metadata": {
            "name": "Phoenix July 24-26, 2023 FortyGuard 72-Hour Capture",
            "location": {
                "city": "Phoenix, AZ",
                "latitude": LAT,
                "longitude": LON,
            },
            "date_range": {
                "start_date": f"{DATES[0]}T00:00:00Z",
                "end_date": f"{DATES[-1]}T23:00:00Z",
            },
            "provenance": {
                "data_source": "fortyguard_live_capture",
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "captured_from": "POST /v1/heatmap (tcm) + POST /v1/env_params",
                "measured_fields": [
                    "fortyguard_2m_ambient_c",
                    "coolest_tile_2m_c",
                    "tile_peak_2m_c",
                    "intra_aoi_spread_c",
                    "relative_humidity_pct",
                    "wet_bulb_temp_c",
                    "cloud_cover_pct",
                ],
                "derived_fields": ["solar_irradiance_w_m2"],
                "modelled_downstream_fields": [
                    "baseline_load_k",
                    "soil_moisture_volumetric",
                    "soil_resistivity_rho",
                    "transformer_thermal_state",
                    "bess_dispatch",
                ],
                "note": (
                    "Frozen live capture for deterministic replay. Solar magnitude uses live "
                    "env_params GHI/cloud data plus solar geometry; FortyGuard exposes no SCADA."
                ),
            },
        },
        "hourly_profile_72h": captured,
    }

    FIXTURE.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {FIXTURE.relative_to(ROOT)} ({len(captured)} hourly rows).")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
