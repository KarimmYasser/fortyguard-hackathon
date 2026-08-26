from __future__ import annotations

import csv
import io
import zipfile

import pytest

from scripts.fetch_ground_truth_comparison import (
    GroundTruthFetchError,
    GroundTruthFetcher,
    build_thermal_comparison,
    parse_caiso_zip,
    parse_eia,
    parse_nsrdb_csv,
    parse_stac,
    parse_synoptic,
)
from src.physics.transformer_thermal import TransformerThermalEngine


def test_synoptic_schema_parsing_accepts_numbered_sensor_sets():
    payload = {
        "STATION": [{
            "STID": "TEST1",
            "NAME": "Roof sensor",
            "OBSERVATIONS": {
                "date_time": ["2024-07-01T00:15:00Z", "2024-07-01T01:00:00Z"],
                "air_temp_set_1": [31.5, 32.0],
                "solar_radiation_set_1": [0, 125.5],
                "relative_humidity_set_1": [22, 20],
            },
        }]
    }
    rows = parse_synoptic(payload)
    assert rows[0] == {
        "timestamp": "2024-07-01T00:00:00Z",
        "station_id": "TEST1",
        "station_name": "Roof sensor",
        "temperature_2m_c": 31.5,
        "solar_ghi_w_m2": 0.0,
        "relative_humidity_pct": 22.0,
    }
    assert rows[1]["solar_ghi_w_m2"] == 125.5


def test_nsrdb_csv_schema_skips_metadata_rows():
    text = """Source,Location ID\nNSRDB,123\nYear,Month,Day,Hour,Minute,Air Temperature,GHI,DNI,DHI\n2024,7,1,0,0,30.2,0,0,0\n2024,7,1,1,0,29.8,10,5,5\n"""
    rows = parse_nsrdb_csv(text)
    assert rows[0]["timestamp"] == "2024-07-01T00:00:00Z"
    assert rows[0]["temperature_2m_c"] == 30.2
    assert rows[1]["solar_ghi_w_m2"] == 10.0


def test_stac_eia_and_caiso_schema_parsing():
    stac = parse_stac({
        "features": [{
            "id": "LC09-test",
            "properties": {"datetime": "2024-07-01T18:00:00Z", "eo:cloud_cover": 3.2},
            "assets": {"lwir11": {"href": "https://example.test/ST_B10.tif"}},
        }]
    }, thermal_key="lwir11")
    assert stac[0]["thermal_asset_url"].endswith("ST_B10.tif")
    assert stac[0]["cloud_cover_pct"] == 3.2

    eia = parse_eia({"response": {"data": [{
        "period": "2024-07-01T00", "respondent": "CISO", "value": "32100", "value-units": "megawatthours",
    }]}})
    assert eia == [{
        "timestamp": "2024-07-01T00:00:00Z",
        "load_mwh": 32100.0,
        "average_load_mw": 32100.0,
        "load_mw": 32100.0,
        "balancing_authority": "CISO",
        "units": "megawatthours",
        "interval_hours": 1,
    }]

    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["INTERVALSTARTTIME_GMT", "TAC_AREA_NAME", "LOAD_TYPE", "MW"])
        writer.writeheader()
        writer.writerow({
            "INTERVALSTARTTIME_GMT": "2024-07-01T00:00:00Z", "TAC_AREA_NAME": "CA ISO-TAC",
            "LOAD_TYPE": "Total Actual Hourly Integrated Load", "MW": "30001.5",
        })
        archive.writestr("result.csv", buffer.getvalue())
    caiso = parse_caiso_zip(output.getvalue())
    assert caiso[0]["load_mw"] == 30001.5
    assert caiso[0]["area"] == "CA ISO-TAC"


def test_missing_credentials_use_explicit_deterministic_mock_fallback():
    fetcher = GroundTruthFetcher(allow_mock=True)
    try:
        first = fetcher.synoptic(34.0522, -118.2437, "2024-07-01", "2024-07-01", None)
        second = fetcher.synoptic(34.0522, -118.2437, "2024-07-01", "2024-07-01", None)
    finally:
        fetcher.close()
    assert first["data_source"] == "mock_fallback"
    assert "SYNOPTIC_API_KEY" in first["error"]
    assert len(first["records"]) == 24
    assert first["records"] == second["records"]


def test_empty_live_result_is_not_mislabeled_as_live():
    fetcher = GroundTruthFetcher(allow_mock=True)
    try:
        result = fetcher._run("empty-provider", list, list)
    finally:
        fetcher.close()
    assert result["data_source"] == "mock_fallback"
    assert "returned no records" in result["error"]


def test_strict_mode_records_missing_provider_without_mocking():
    fetcher = GroundTruthFetcher(allow_mock=False)
    try:
        result = fetcher.synoptic(34.0522, -118.2437, "2024-07-01", "2024-07-01", None)
    finally:
        fetcher.close()
    assert result["data_source"] == "unavailable"
    assert result["records"] == []
    assert "SYNOPTIC_API_KEY" in result["error"]


def test_synoptic_api_error_message_is_exposed():
    with pytest.raises(GroundTruthFetchError, match="does not have access"):
        parse_synoptic({"SUMMARY": {"RESPONSE_CODE": 403, "RESPONSE_MESSAGE": "token does not have access"}})


def test_comparison_is_mathematically_identical_to_ieee_solver():
    weather = [
        {"timestamp": "2024-07-01T00:00:00Z", "temperature_2m_c": 35.0, "solar_ghi_w_m2": 0.0},
        {"timestamp": "2024-07-01T01:00:00Z", "temperature_2m_c": 37.0, "solar_ghi_w_m2": 200.0},
        {"timestamp": "2024-07-01T02:00:00Z", "temperature_2m_c": 39.0, "solar_ghi_w_m2": 500.0},
    ]
    load = [
        {"timestamp": "2024-07-01T00:00:00Z", "load_mw": 12.5},
        {"timestamp": "2024-07-01T01:00:00Z", "load_mw": 20.0},
        {"timestamp": "2024-07-01T02:00:00Z", "load_mw": 25.0},
    ]
    result = build_thermal_comparison(
        weather, load, transformer_rating_mw=25.0, load_evidence_class="asset_scada"
    )

    forecast = [{
        "timestamp": row["timestamp"],
        "fortyguard_2m_ambient_c": row["temperature_2m_c"],
        "solar_irradiance_w_m2": row["solar_ghi_w_m2"],
    } for row in weather]
    direct = TransformerThermalEngine().simulate_trajectory(
        "direct", forecast, [0.5, 0.8, 1.0]
    )

    assert result["load_ratio_k"] == [0.5, 0.8, 1.0]
    assert result["peak_top_oil_c"] == direct.peak_top_oil_c
    assert result["peak_hot_spot_c"] == direct.peak_hot_spot_c
    assert result["total_loss_of_life_hours"] == direct.total_loss_of_life_hours
    assert [row["t_hot_spot_c"] for row in result["steps"]] == [row.t_hot_spot_c for row in direct.steps]
    assert result["load_mapping"] == "asset MW / transformer nameplate MW"


def test_regional_load_is_shape_normalized_not_treated_as_transformer_mw():
    weather = [
        {"timestamp": "2024-07-01T00:00:00Z", "temperature_2m_c": 35, "solar_ghi_w_m2": 0},
        {"timestamp": "2024-07-01T01:00:00Z", "temperature_2m_c": 36, "solar_ghi_w_m2": 50},
    ]
    regional = [
        {"timestamp": "2024-07-01T00:00:00Z", "load_mw": 20_000},
        {"timestamp": "2024-07-01T01:00:00Z", "load_mw": 40_000},
    ]
    result = build_thermal_comparison(
        weather, regional, transformer_rating_mw=25, regional_peak_load_ratio=1.1
    )
    assert result["load_evidence_class"] == "regional_balancing_authority"
    assert result["load_ratio_k"] == [0.55, 1.1]
    assert max(result["load_ratio_k"]) == 1.1
    assert "normalized regional" in result["load_mapping"]


def test_comparison_requires_overlapping_utc_hours():
    with pytest.raises(GroundTruthFetchError, match="no overlapping"):
        build_thermal_comparison(
            [{"timestamp": "2024-07-01T00:00:00Z", "temperature_2m_c": 30}],
            [{"timestamp": "2024-07-02T00:00:00Z", "load_mw": 10}],
        )
