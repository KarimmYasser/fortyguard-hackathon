"""
Backfill city / analysis_date onto microclimate_parcel_store rows written
before those fields were recorded.

The parcel table never had a column for either, and rows predating the GeoJSON
properties convention carry only coordinates and a wall-clock scanned_at. The
catalog date is what makes a stored scan re-solvable, and guessing it would
silently attribute one day's physics to another.

It does not have to be guessed. Every scan's hours are still in api_call_cache
with their start_date, so (latitude, longitude, measured peak) identifies the
date from stored evidence. A row is only rewritten when that match is unique;
anything ambiguous is reported and left alone.

Usage:
    python3 scripts/backfill_parcel_properties.py           # dry run
    python3 scripts/backfill_parcel_properties.py --apply
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

import httpx
from dotenv import load_dotenv

load_dotenv(".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# Labels must match the scan modal's presets so a backfilled row is
# indistinguishable from a freshly stored one.
KNOWN_SITES = {
    (33.4484, -112.0740): "Phoenix, AZ (Substation TX-04)",
    (37.3382, -121.8863): "San Jose, CA (Diridon Energy Hub)",
    (36.1699, -115.1398): "Las Vegas, NV (Downtown Feeder)",
    (29.7604, -95.3698): "Houston, TX (Energy Corridor)",
}

TOLERANCE_C = 0.005  # temps are stored rounded to 2dp


def aoi_center(aoi: dict):
    try:
        ring = aoi["features"][0]["geometry"]["coordinates"][0]
        return round(sum(p[1] for p in ring[:4]) / 4, 4), round(sum(p[0] for p in ring[:4]) / 4, 4)
    except Exception:
        return None


def build_date_index() -> dict:
    """(lat, lon) -> {date: peak_mean_c} reconstructed from cached tcm hours."""
    rows = httpx.get(
        f"{SUPABASE_URL}/rest/v1/api_call_cache",
        params={"select": "request_params,response_payload", "endpoint": "eq./v1/heatmap", "limit": "5000"},
        headers=HEADERS,
        timeout=60,
    ).json()

    groups = collections.defaultdict(list)
    for r in rows:
        rp, pl = r.get("request_params"), r.get("response_payload")
        if isinstance(rp, str):
            rp = json.loads(rp)
        if isinstance(pl, str):
            pl = json.loads(pl)
        if not isinstance(rp, dict):
            continue
        date = (rp.get("date_time") or {}).get("start_date")
        center = aoi_center(rp.get("polygon_aoi") or {})
        stats = ((pl or {}).get("stats_data") or {}).get("temperature_stats") or {}
        if not date or not center or stats.get("mean") is None:
            continue
        groups[(center[0], center[1], date)].append(float(stats["mean"]))

    index = collections.defaultdict(dict)
    for (lat, lon, date), means in groups.items():
        # A single probed hour is not a scan and must not be matched against one.
        if len(means) < 12:
            continue
        index[(lat, lon)][date] = round(max(means), 2)
    return index


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write the changes")
    args = ap.parse_args()

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase credentials missing.")
        return 1

    index = build_date_index()
    print(f"Reconstructed {sum(len(v) for v in index.values())} dated scan groups from api_call_cache.\n")

    parcels = httpx.get(
        f"{SUPABASE_URL}/rest/v1/microclimate_parcel_store",
        params={"select": "*", "limit": "1000"},
        headers=HEADERS,
        timeout=60,
    ).json()

    fixable, ambiguous, already = [], [], 0

    for p in parcels:
        geom = p.get("polygon_geojson") or {}
        if isinstance(geom, str):
            geom = json.loads(geom)
        if (geom.get("properties") or {}).get("analysis_date"):
            already += 1
            continue

        coords = geom.get("coordinates")
        if not (isinstance(coords, list) and len(coords) == 2):
            ambiguous.append((p["parcel_id"], "no coordinates stored"))
            continue

        lat, lon = round(coords[1], 4), round(coords[0], 4)
        peak = p.get("convective_temp_2m_c")
        candidates = [d for d, v in index.get((lat, lon), {}).items() if abs(v - peak) <= TOLERANCE_C]

        if len(candidates) == 1:
            fixable.append((p, geom, lat, lon, candidates[0]))
        else:
            ambiguous.append(
                (p["parcel_id"], f"{len(candidates)} dates match {peak}C at {lat},{lon}")
            )

    print(f"already compliant : {already}")
    print(f"recoverable       : {len(fixable)}")
    print(f"NOT recoverable   : {len(ambiguous)}\n")

    for p, geom, lat, lon, date in fixable:
        print(f"  {p['parcel_id']:<22} -> {date}  {KNOWN_SITES.get((lat, lon), f'{lat},{lon}')}")
    for pid, why in ambiguous:
        print(f"  SKIP {pid:<22} {why}")

    if not args.apply:
        print("\nDry run. Re-run with --apply to write.")
        return 0

    written = 0
    for p, geom, lat, lon, date in fixable:
        geom["properties"] = {
            **(geom.get("properties") or {}),
            "city": KNOWN_SITES.get((lat, lon), f"{lat}, {lon}"),
            "analysis_date": date,
            "latitude": lat,
            "longitude": lon,
            "peak_2m_ambient_c": p["convective_temp_2m_c"],
            "data_source": "fortyguard_live",
            # Say plainly that this was reconstructed rather than recorded.
            "backfilled_from": "api_call_cache",
        }
        r = httpx.patch(
            f"{SUPABASE_URL}/rest/v1/microclimate_parcel_store",
            params={"parcel_id": f"eq.{p['parcel_id']}"},
            json={"polygon_geojson": geom},
            headers=HEADERS,
            timeout=30,
        )
        if r.status_code in (200, 204):
            written += 1
        else:
            print(f"  FAILED {p['parcel_id']}: {r.status_code} {r.text[:120]}")

    print(f"\nBackfilled {written}/{len(fixable)} rows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
