from __future__ import annotations

import pytest

from src.db.database import HybridDatabaseManager
from src.db.models import ValidationRunRecord


@pytest.mark.asyncio
async def test_validation_runs_are_immutable_and_queryable(tmp_path):
    database = HybridDatabaseManager(str(tmp_path / "validation.db"))
    record = ValidationRunRecord(
        validation_id="sha256-id",
        scenario_id="phoenix",
        provider="iem_asos",
        evidence_class="in-situ station observation",
        baseline_identity="baseline",
        reference_identity="reference",
        configuration={"source": "iem"},
        report={"metrics": {"temperature_2m": {"mae": 1.0}}},
    )
    await database.save_validation_run(record)
    await database.save_validation_run(record)
    rows = await database.get_validation_runs("phoenix")
    assert len(rows) == 1
    assert rows[0]["configuration"] == {"source": "iem"}
    assert rows[0]["report"]["metrics"]["temperature_2m"]["mae"] == 1.0
    status = await database.get_database_status()
    assert status["counts"]["validation_runs"] == 1
