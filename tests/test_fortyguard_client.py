import pytest
from src.api.fortyguard_client import (
    AsyncFortyGuardClient,
    FortyGuardClient,
    load_phoenix_fixture,
)

@pytest.mark.asyncio
async def test_async_fortyguard_client_mock():
    client = AsyncFortyGuardClient(mock_mode=True)
    assert client.mock_mode is True

    # Test heatmap creation
    res = await client.create_heatmap(
        polygon_aoi={"type": "Polygon", "coordinates": []},
        start_date="2023-07-24",
        analytic_type="tcm",
    )
    assert isinstance(res, dict)
    assert "activity_id" in res
    assert "result" in res

    # Test environmental parameters
    env = await client.environmental_parameters(
        latitude=33.4484,
        longitude=-112.0740,
        temperature=42.7,
        start_date="2023-07-19",
    )
    assert "result" in env
    assert "solar_irradiance" in env["result"]
    assert env["result"]["solar_irradiance"] > 0

    # Test 12h forecast. The fixture is a real cached FortyGuard capture
    # (2023-07-19 downtown Phoenix), so assert on physical properties rather
    # than on literals that a re-capture would legitimately change.
    forecast = await client.get_12h_forecast()
    assert len(forecast) == 12

    temps = [h["fortyguard_2m_ambient_c"] for h in forecast]
    assert all(35.0 < t < 50.0 for t in temps), temps
    # Heat-of-day window: it should warm from the 06:00 start toward the peak.
    assert max(temps) > temps[0]
    assert max(temps) > 40.0, "benchmark scenario must exceed the 40C threshold"

    # Delta is measured spatial spread within the AOI, not an assumed constant.
    assert all(h["intra_aoi_spread_c"] >= 0 for h in forecast)

    # Test persistence
    persist = await client.get_persistence_and_exceedance()
    assert 0.0 <= persist["persistence_hours_p40"] <= 24.0
    assert persist["exceedance_degree_hours_h40"] > 0
    assert persist["thermal_soak_index_tsi"] > 0


def test_sync_fortyguard_client_mock():
    client = FortyGuardClient(mock_mode=True)
    forecast = client.get_12h_forecast()
    assert len(forecast) == 12
    assert 30.0 < forecast[0]["fortyguard_2m_ambient_c"] < 45.0


def test_fixture_is_a_real_api_capture():
    """
    Guards the regression this fixture was created to fix: it used to be
    hand-authored (peak 47.6C, P40 7.17h) while being documented as cached
    ground truth, so replay mode and live mode disagreed.
    """
    fixture = load_phoenix_fixture()
    prov = fixture["scenario_metadata"].get("provenance", {})
    assert prov.get("data_source") == "fortyguard_live", "fixture must be a real API capture"

    peak = max(h["fortyguard_2m_ambient_c"] for h in fixture["hourly_forecast_12h"])
    assert peak != 47.6, "47.6C was the old synthetic peak"

    metrics = fixture["scenario_metadata"]["persistence_metrics"]
    assert metrics["persistence_hours_p40"] != 7.17, "7.17h was the old synthetic value"


def test_load_phoenix_fixture():
    fixture = load_phoenix_fixture()
    assert "scenario_metadata" in fixture
    assert fixture["scenario_metadata"]["location"]["city"] == "Phoenix"


def test_client_base_url_normalization():
    client = AsyncFortyGuardClient(base_url="https://api.fortyguard.com/v1", mock_mode=True)
    assert client.base_url == "https://api.fortyguard.com"
    assert hasattr(client, "fetch_api_key_usage")
    assert hasattr(client, "fetch_api_key_custom_usage")

