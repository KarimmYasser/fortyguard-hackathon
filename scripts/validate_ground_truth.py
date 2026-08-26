#!/usr/bin/env python3
"""Compare the bundled FortyGuard benchmark with public reference data."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api.fortyguard_client import load_phoenix_fixture
from src.api.nsrdb_ground_truth_client import (
    AsyncNSRDBGroundTruthClient,
    NSRDBGroundTruthError,
)
from src.data_science.ground_truth_pipeline import GroundTruthValidationPipeline
from src.data_science.ground_truth_validation import (
    GroundTruthValidationError,
    validate_fortyguard_curve,
)


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", choices=("auto", "iem", "iem-metro", "open-meteo", "nsrdb"), default="auto"
    )
    parser.add_argument("--metro", choices=("phoenix", "houston", "las_vegas", "san_jose"), default="phoenix")
    parser.add_argument("--station", default="PHX", help="IEM station (default: PHX/KPHX)")
    parser.add_argument("--latitude", type=float, default=33.4484)
    parser.add_argument("--longitude", type=float, default=-112.0740)
    parser.add_argument("--start-date", default="2023-07-19")
    parser.add_argument("--end-date", default="2023-07-19")
    parser.add_argument("--minimum-pairs", type=int, default=6)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    baseline = load_phoenix_fixture()["hourly_forecast_12h"]
    if args.source == "iem-metro":
        report = await GroundTruthValidationPipeline().validate_metro(
            baseline, metro=args.metro, start_date=args.start_date,
            end_date=args.end_date, minimum_pairs=args.minimum_pairs,
        )
    elif args.source == "nsrdb":
        truth = await AsyncNSRDBGroundTruthClient().fetch_hourly(
            args.latitude, args.longitude, args.start_date, args.end_date
        )
        report = validate_fortyguard_curve(
            baseline, truth, minimum_pairs=args.minimum_pairs
        )
        report["selection"] = {
            "requested_source": "nsrdb", "selected_source": "nsrdb",
            "fallback_used": False, "failures": [],
        }
    else:
        report = await GroundTruthValidationPipeline().validate(
            baseline,
            latitude=args.latitude,
            longitude=args.longitude,
            start_date=args.start_date,
            end_date=args.end_date,
            station=args.station,
            minimum_pairs=args.minimum_pairs,
            source=args.source,
            scenario_id="phoenix_heatwave_july_2023",
        )
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (NSRDBGroundTruthError, GroundTruthValidationError) as exc:
        raise SystemExit(f"validation failed: {exc}") from None
