#!/usr/bin/env python3
"""Verify deployed validation routes after Vercel/Supabase configuration."""

from __future__ import annotations

import argparse
import sys

import httpx


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", help="e.g. https://www.thermal-sentinel-grid.live")
    parser.add_argument("--live", action="store_true", help="also invoke key-free live IEM validation")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")
    checks = [
        ("GET", "/api/v1/health", None),
        ("GET", "/api/v1/benchmark/ground-truth-comparison", None),
        ("GET", "/api/v1/validation/metro/phoenix", None),
        ("GET", "/api/v1/db/validation-runs?limit=1", None),
    ]
    if args.live:
        checks.append(("GET", "/api/v1/validation/phoenix-2023?source=iem&station=PHX", None))
    failed = False
    with httpx.Client(timeout=90, follow_redirects=True) as client:
        for method, path, payload in checks:
            try:
                response = client.request(method, f"{base}{path}", json=payload)
                response.raise_for_status()
                body = response.json()
                if path.startswith("/api/v1/benchmark/ground-truth-comparison"):
                    metrics = body.get("metrics", {}).get("temperature_2m", {})
                    if metrics.get("n_pairs", 0) < 6 or metrics.get("coverage_pct", 0) < 80:
                        raise RuntimeError("comparison did not pass pair/coverage gates")
                    if metrics.get("pearson_r") is None:
                        raise RuntimeError("comparison did not expose correlation")
                    if body.get("comparison", {}).get("time_alignment") is None:
                        raise RuntimeError("comparison omitted clock normalization provenance")
                elif path.startswith("/api/v1/validation/metro/"):
                    if body.get("station_count", 0) < 2:
                        raise RuntimeError("metro comparison did not expose multiple stations")
                    if body.get("credits_spent") != 0:
                        raise RuntimeError("metro replay was not zero-credit")
                elif path.startswith("/api/v1/db/validation-runs") and not isinstance(body, list):
                    raise RuntimeError("validation-runs endpoint did not return a list")
                print(f"PASS {response.status_code} {path}")
            except Exception as exc:
                failed = True
                print(f"FAIL {path}: {exc}", file=sys.stderr)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
