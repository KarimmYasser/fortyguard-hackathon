"""
Guards for the live-scan path.

Every bug covered here shipped to production and was visible in the UI as a
confident, wrong number - which is worse than an obvious blank.
"""
from __future__ import annotations

import ast
import inspect
from pathlib import Path

import pytest

from src.server.routes.sandbox import SandboxSimulationRequest, run_sandbox_simulation
from src.server.routes.scan import ScanRequest, _parcel_id_for_scan, execute_spatial_scan

ROOT = Path(__file__).resolve().parents[1]


class TestScanPersistenceIsMeasured:
    def test_identical_scan_inputs_reuse_the_same_parcel_identity(self):
        request = ScanRequest(
            city="Phoenix, AZ",
            latitude=33.4484,
            longitude=-112.074,
            start_date="2023-07-19",
            analytic_type="tcm",
            threshold_c=40.0,
        )
        first = _parcel_id_for_scan(request, "2023-07-19")
        second = _parcel_id_for_scan(request.model_copy(), "2023-07-19")

        assert first == second
        assert first.startswith("PARCEL-PHO-")

    def test_materially_different_scan_inputs_get_different_parcel_identities(self):
        phoenix = ScanRequest(city="Phoenix, AZ", latitude=33.4484, longitude=-112.074)
        houston = ScanRequest(city="Houston, TX", latitude=29.7604, longitude=-95.3698)

        assert _parcel_id_for_scan(phoenix, "2023-07-19") != _parcel_id_for_scan(
            houston, "2023-07-19"
        )
        assert _parcel_id_for_scan(phoenix, "2023-07-19") != _parcel_id_for_scan(
            phoenix, "2024-07-15"
        )

    def test_parcel_record_is_not_built_from_hardcoded_constants(self):
        """
        The scan route used to persist surface_temp_c=58.2 /
        convective_temp_2m_c=42.74 / asphalt_heat_trap_delta=1.1 for every
        scan, so a Houston scan was stored as Phoenix constants.
        """
        src = inspect.getsource(execute_spatial_scan)
        tree = ast.parse(inspect.cleandoc(src))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "MicroclimateParcelRecord"):
                continue
            for kw in node.keywords:
                if kw.arg in ("surface_temp_c", "convective_temp_2m_c", "asphalt_heat_trap_delta"):
                    assert not isinstance(kw.value, ast.Constant), (
                        f"MicroclimateParcelRecord.{kw.arg} is a hardcoded literal "
                        f"({getattr(kw.value, 'value', '?')}); it must come from the scan."
                    )

    def test_scan_forwards_the_requested_date_to_persistence(self):
        """
        Omitting start_date made persistence default to the pinned Phoenix
        benchmark date, so a Houston 2025-07-15 scan returned results stamped
        2023-07-19.
        """
        src = inspect.getsource(execute_spatial_scan)
        tree = ast.parse(inspect.cleandoc(src))
        calls = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and getattr(n.func, "attr", "") == "get_persistence_and_exceedance"
        ]
        assert calls, "scan no longer calls get_persistence_and_exceedance"
        for c in calls:
            assert "start_date" in {kw.arg for kw in c.keywords}, (
                "get_persistence_and_exceedance must receive start_date, "
                "otherwise every scan is stamped with the Phoenix benchmark date."
            )

    def test_scan_does_not_read_air_temperature_from_env_params(self):
        """
        env_params.heat_index_celsius is not on the Celsius scale despite the
        name - Houston returns 99.1 there against a 39.8 apparent temperature.
        2m air temperature comes from the tcm analytic only.
        """
        # Check the code, not the prose: this function's docstring names the
        # very field it must not read, so a substring scan would self-trip.
        tree = ast.parse(inspect.cleandoc(inspect.getsource(execute_spatial_scan)))
        fn = tree.body[0]
        if (fn.body and isinstance(fn.body[0], ast.Expr)
                and isinstance(fn.body[0].value, ast.Constant)):
            fn.body = fn.body[1:]  # drop the docstring
        literals = {
            n.value for n in ast.walk(ast.Module(body=fn.body, type_ignores=[]))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }
        attrs = {n.attr for n in ast.walk(ast.Module(body=fn.body, type_ignores=[]))
                 if isinstance(n, ast.Attribute)}
        assert "heat_index_celsius" not in literals | attrs
        assert "get_12h_forecast" in attrs, "2m series must come from the tcm-backed forecast"


class TestSandboxLiveBinding:
    @pytest.mark.asyncio
    async def test_benchmark_mode_is_unchanged(self):
        res = await run_sandbox_simulation(SandboxSimulationRequest())
        assert res["scan_binding"]["mode"] == "benchmark_replay"
        assert res["economic_evaluation"]["net_avoided_loss_usd"] == pytest.approx(2565139.66, abs=1.0)

    @pytest.mark.asyncio
    async def test_live_binding_never_silently_reports_phoenix(self, monkeypatch):
        """
        If the live profile can't be fetched, the endpoint must fail loudly.
        Falling through to the Phoenix curve would label benchmark physics as
        the user's own scan.
        """
        from src.api import fortyguard_client as fc
        from fastapi import HTTPException

        async def _empty(*a, **k):
            return []

        monkeypatch.setattr(fc.AsyncFortyGuardClient, "get_12h_forecast", _empty)
        with pytest.raises(HTTPException) as exc:
            await run_sandbox_simulation(SandboxSimulationRequest(
                latitude=29.7604, longitude=-95.3698, analysis_date="2025-07-15",
            ))
        assert exc.value.status_code == 502

    @pytest.mark.asyncio
    async def test_live_binding_uses_measured_spread_over_slider(self, monkeypatch):
        from src.api import fortyguard_client as fc

        async def _fake(*a, **k):
            return [
                {
                    "hour_index": 6 + i, "time_label": f"{6+i}:00",
                    "fortyguard_2m_ambient_c": 30.0 + i,
                    "coolest_tile_2m_c": 30.0 + i - 0.5,
                    "intra_aoi_spread_c": 0.5,
                    "solar_irradiance_w_m2": 400.0 + 10 * i,
                    "data_source": "fortyguard_live",
                }
                for i in range(12)
            ]

        monkeypatch.setattr(fc.AsyncFortyGuardClient, "get_12h_forecast", _fake)
        res = await run_sandbox_simulation(SandboxSimulationRequest(
            latitude=29.7604, longitude=-95.3698, intra_aoi_spread_c=7.5,
        ))
        b = res["scan_binding"]
        assert b["mode"] == "live_scan"
        # The 7.5 slider value must not override the measured 0.5.
        assert b["measured_intra_aoi_spread_c"] == pytest.approx(0.5)
        assert b["peak_2m_ambient_c"] == pytest.approx(41.0)

    @pytest.mark.asyncio
    async def test_live_binding_with_presupplied_forecast_skips_network(self):
        """Pre-supplied hourly forecast runs immediately without calling FortyGuard client."""
        forecast = [
            {
                "hour_index": i,
                "time_label": f"{6+i:02d}:00",
                "timestamp": f"2024-07-15T{6+i:02d}:00:00-07:00",
                "fortyguard_2m_ambient_c": 38.0 + (i * 0.5),
                "coolest_tile_2m_c": 36.5 + (i * 0.5),
                "intra_aoi_spread_c": 1.5,
                "solar_irradiance_w_m2": 700.0,
                "data_source": "fortyguard_live",
            }
            for i in range(12)
        ]
        persistence = {
            "persistence_hours_p40": 8.5,
            "exceedance_hours_e40": 8.5,
            "exceedance_degree_hours_h40": 14.2,
            "thermal_soak_index_tsi": 2.8,
            "data_source": "fortyguard_live",
        }
        res = await run_sandbox_simulation(SandboxSimulationRequest(
            city="San Jose, CA",
            latitude=37.3382,
            longitude=-121.8863,
            analysis_date="2024-07-15",
            hourly_forecast=forecast,
            persistence_metrics=persistence,
        ))
        assert res["status"] == "success"
        b = res["scan_binding"]
        assert b["mode"] == "live_scan"
        assert b["city"] == "San Jose, CA"
        assert b["peak_2m_ambient_c"] == pytest.approx(43.5)
        assert b["measured_intra_aoi_spread_c"] == pytest.approx(1.5)
        assert len(res["timeline_steps"]) == 12
        assert res["baseline_summary"]["peak_hot_spot_c"] > 0
        assert res["economic_evaluation"]["net_avoided_loss_usd"] > 0

    @pytest.mark.asyncio
    async def test_presupplied_forecast_too_short_raises_502(self):
        """Fewer than 2 valid hours in pre-supplied forecast raises 502."""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await run_sandbox_simulation(SandboxSimulationRequest(
                hourly_forecast=[{"fortyguard_2m_ambient_c": 39.0}],
            ))
        assert exc.value.status_code == 502


class TestUiDoesNotFabricateOnZero:
    def test_scan_modal_has_no_falsy_fallbacks(self):
        """
        `value || '12.0'` rendered Phoenix's 12.0h whenever the real reading was
        0.0 - and Houston genuinely measures P40 = 0.0h.
        """
        raw = (ROOT / "frontend/src/components/LiveApiScanModal.tsx").read_text()
        # Strip // comments - the fix is documented in one, which would self-trip.
        src = "\n".join(ln for ln in raw.splitlines() if not ln.strip().startswith("//"))
        for bad in ("|| '12.0'", "|| '42.7'", "|| '960'", "|| '24.6'"):
            assert bad not in src, f"falsy fallback {bad} fabricates a Phoenix constant on a real zero"
