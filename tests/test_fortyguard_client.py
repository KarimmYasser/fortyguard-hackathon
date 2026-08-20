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
        temperature=47.6,
        start_date="2023-07-24",
    )
    assert "result" in env
    assert "solar_irradiance" in env["result"]
    assert env["result"]["solar_irradiance"] > 0

    # Test 12h forecast
    forecast = await client.get_12h_forecast()
    assert len(forecast) == 12
    assert forecast[7]["fortyguard_2m_ambient_c"] == 47.6
    assert forecast[7]["microclimate_delta_c"] == 4.5

    # Test persistence
    persist = await client.get_persistence_and_exceedance()
    assert persist["persistence_hours_p40"] == 7.17
    assert persist["exceedance_degree_hours_h40"] == 34.25


def test_sync_fortyguard_client_mock():
    client = FortyGuardClient(mock_mode=True)
    forecast = client.get_12h_forecast()
    assert len(forecast) == 12
    assert forecast[0]["fortyguard_2m_ambient_c"] == 34.2


def test_load_phoenix_fixture():
    fixture = load_phoenix_fixture()
    assert "scenario_metadata" in fixture
    assert fixture["scenario_metadata"]["location"]["city"] == "Phoenix"


def test_client_base_url_normalization():
    client = AsyncFortyGuardClient(base_url="https://api.fortyguard.com/v1", mock_mode=True)
    assert client.base_url == "https://api.fortyguard.com"
    assert hasattr(client, "fetch_api_key_usage")
    assert hasattr(client, "fetch_api_key_custom_usage")

