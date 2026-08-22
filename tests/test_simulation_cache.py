"""
A solve must survive being asked for twice.

`simulation_runs` keeps scalars for the audit trail but cannot reconstruct a
trajectory, so the full payload has to be persisted or the work is silently
recomputed and discarded on every revisit.
"""

import uuid

import pytest


def _unique_mva() -> float:
    """
    The cache is durable by design, so a fixed input is a hit on the second run
    of the suite. Vary an input that changes the key without changing the code
    path, so 'first call is a miss' stays true on a warm database.
    """
    return 20.0 + (uuid.uuid4().int % 10_000_000) / 1_000_000.0

from src.server.routes.sandbox import (
    SandboxSimulationRequest,
    _simulation_cache_key,
    run_sandbox_simulation,
)


class TestSimulationResultPersistence:

    @pytest.mark.asyncio
    async def test_identical_inputs_replay_the_stored_solve(self):
        req = SandboxSimulationRequest(transformer_mva=_unique_mva(), bess_capacity_mwh=13.0)
        first = await run_sandbox_simulation(req)
        second = await run_sandbox_simulation(req)

        assert first["cache"]["hit"] is False
        assert second["cache"]["hit"] is True
        assert second["cache"]["key"] == _simulation_cache_key(req)
        assert second["timeline_steps"] == first["timeline_steps"]
        assert second["economic_evaluation"] == first["economic_evaluation"]
        assert second["safety_gate_verdict"] == first["safety_gate_verdict"]

    @pytest.mark.asyncio
    async def test_different_inputs_do_not_collide(self):
        a = await run_sandbox_simulation(SandboxSimulationRequest(transformer_mva=_unique_mva()))
        b = await run_sandbox_simulation(SandboxSimulationRequest(transformer_mva=_unique_mva() + 20.0))
        assert a["cache"]["key"] != b["cache"]["key"]
        assert (
            a["economic_evaluation"]["net_avoided_loss_usd"]
            != b["economic_evaluation"]["net_avoided_loss_usd"]
        )

    @pytest.mark.asyncio
    async def test_location_is_part_of_the_identity(self):
        """Two cities must never share a cached solve."""
        base = dict(analysis_date="2024-07-15")
        hou = SandboxSimulationRequest(latitude=29.78, longitude=-95.64, city="Houston", **base)
        phx = SandboxSimulationRequest(latitude=33.45, longitude=-112.07, city="Phoenix", **base)
        assert _simulation_cache_key(hou) != _simulation_cache_key(phx)

    @pytest.mark.asyncio
    async def test_the_stored_payload_is_replayable_not_a_summary(self, monkeypatch):
        """A cached entry missing timeline_steps cannot rebase the dashboard."""
        from src.server.routes import sandbox as sbx

        captured = {}

        async def _spy(record):
            captured["record"] = record

        monkeypatch.setattr(sbx.db_manager, "save_cached_api_call", _spy)
        await run_sandbox_simulation(SandboxSimulationRequest(transformer_mva=_unique_mva()))

        rec = captured.get("record")
        assert rec is not None, "the solve was never persisted"
        assert rec.endpoint == "sandbox/simulate"
        assert rec.expires_at is None, "a solved result must not expire"

        payload = rec.response_payload
        for key in (
            "timeline_steps",
            "baseline_summary",
            "mitigated_summary",
            "economic_evaluation",
            "safety_gate_verdict",
        ):
            assert key in payload, f"stored payload cannot be replayed without {key}"
        assert len(payload["timeline_steps"]) > 0

    @pytest.mark.asyncio
    async def test_a_failed_write_does_not_break_the_response(self, monkeypatch):
        """Persistence is best-effort on the response path; it must not 500."""
        from src.server.routes import sandbox as sbx

        async def _boom(record):
            raise RuntimeError("supabase down")

        monkeypatch.setattr(sbx.db_manager, "save_cached_api_call", _boom)
        monkeypatch.setattr(sbx.db_manager, "get_cached_api_call", lambda k: _none())

        async def _none():
            return None

        res = await run_sandbox_simulation(SandboxSimulationRequest(transformer_mva=_unique_mva()))
        assert res["status"] == "success"
        assert res["cache"]["hit"] is False
