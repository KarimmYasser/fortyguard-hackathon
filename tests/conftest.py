"""
Shared pytest configuration for Thermal Sentinel Grid.

Makes the suite hermetic: without this, tests instantiate the real
AsyncFortyGuardClient, which hits the live FortyGuard API. That made the suite
non-deterministic and slow (10+ minutes, with cascading failures whenever the
remote task queue sat in 'processing' until the 600s poll deadline).

Tests exercise our own physics/agent/persistence logic, so they run against the
bundled Phoenix July 2023 fixture instead. Live-API behaviour is verified
separately, not in unit tests.
"""

import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def _force_fixture_backed_fortyguard():
    """Force the FortyGuard client into fixture mode for the whole suite."""
    previous = os.environ.get("MOCK_FORTYGUARD_API")
    os.environ["MOCK_FORTYGUARD_API"] = "true"
    yield
    if previous is None:
        os.environ.pop("MOCK_FORTYGUARD_API", None)
    else:
        os.environ["MOCK_FORTYGUARD_API"] = previous


@pytest.fixture(autouse=True)
def _isolate_supabase(monkeypatch):
    """
    Keep unit tests off the real Supabase project.

    The hybrid read path is Supabase-first, so without this a developer with
    real credentials in .env would have production rows merged into local
    assertions (and test writes would land in the production tables).
    """
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_KEY", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "")
