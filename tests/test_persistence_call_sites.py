"""Guards against silently-broken database writes.

Every persistence call in this codebase is deliberately non-fatal: a failed
insert must never take down a physics endpoint. The cost of that choice is that
a typo'd attribute or a renamed method produces a working HTTP 200 and no data,
which is how `hour_step`, `save_chance_constrained_opf_log` and a fire-and-forget
`create_task` all survived in production.

These tests make that class of defect fail in CI instead.
"""
from __future__ import annotations

import ast
import inspect
import logging
import pathlib

import pytest

from src.db.database import db_manager

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _db_manager_calls():
    """Yield (file, lineno, method, is_awaited) for every db_manager.* call."""
    for path in (ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text())
        parents = {c: n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)):
                continue
            target = node.func.value
            if isinstance(target, ast.Name) and target.id == "db_manager":
                awaited = isinstance(parents.get(node), ast.Await)
                yield path.relative_to(ROOT), node.lineno, node.func.attr, awaited


def test_every_db_manager_method_exists():
    """A renamed manager method should fail here, not in a Vercel log."""
    missing = [
        f"{f}:{line} -> db_manager.{meth}()"
        for f, line, meth, _ in _db_manager_calls()
        if not hasattr(db_manager, meth)
    ]
    assert not missing, "Calls to non-existent db_manager methods:\n  " + "\n  ".join(missing)


def test_async_db_writes_are_awaited():
    """Un-awaited coroutines never run, and on serverless are silently cancelled."""
    unawaited = [
        f"{f}:{line} -> db_manager.{meth}()"
        for f, line, meth, awaited in _db_manager_calls()
        if hasattr(db_manager, meth)
        and inspect.iscoroutinefunction(getattr(db_manager, meth))
        and not awaited
    ]
    assert not unawaited, "Async db_manager writes not awaited:\n  " + "\n  ".join(unawaited)


def test_cbf_gate_buffers_certificates_instead_of_scheduling():
    """Fire-and-forget writes cannot complete once a serverless lambda freezes."""
    # Parse rather than grep: the file explains in prose why create_task was
    # removed, and a substring check would match its own comment.
    tree = ast.parse((ROOT / "src" / "safety" / "cbf_gate.py").read_text())
    scheduled = [
        node.lineno
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"create_task", "ensure_future"}
    ]
    assert not scheduled, (
        f"cbf_gate schedules background persistence at line(s) {scheduled}; buffer "
        "the record and let the async caller await persist_pending_certificates()."
    )


@pytest.mark.asyncio
async def test_bess_record_fields_match_the_solver_output(caplog):
    """The BESS route read five attribute names the solver never exposed."""
    from src.db.models import BESSDegradationRecord
    from src.physics.bess_electro_thermal import BESSElectroThermalEngine

    steps = BESSElectroThermalEngine().simulate_dispatch_trajectory(
        ambient_temps_c=[40.0] * 4,
        dispatch_powers_mw=[2.0, 4.0, 3.0, 1.0],
        initial_soc=85.0,
        initial_core_temp_c=32.0,
    )
    assert steps, "solver returned no steps"

    # Construct exactly as the route does; an attribute rename raises here.
    for idx, r in enumerate(steps):
        BESSDegradationRecord(
            bess_id="BESS-TEST",
            hour_step=idx,
            ambient_c=r.ambient_temp_c,
            dispatch_power_mw=r.discharge_power_mw,
            core_temp_c=r.core_temp_c,
            surface_temp_c=r.surface_temp_c,
            soc_pct=r.state_of_charge_pct,
            soh_pct=r.state_of_health_pct,
            degradation_cost_usd=r.hourly_degradation_cost_usd,
        )


@pytest.mark.asyncio
async def test_replay_emits_no_persistence_warnings(caplog):
    """A clean replay must not log a single 'Failed to persist' warning."""
    from src.replay.phoenix_heatwave_replay import PhoenixHeatwaveReplayEngine

    engine = PhoenixHeatwaveReplayEngine()
    with caplog.at_level(logging.WARNING):
        engine.generate_replay_dataset()

    failures = [r.getMessage() for r in caplog.records if "Failed to persist" in r.getMessage()]
    assert not failures, "Persistence failures during replay:\n  " + "\n  ".join(failures)
