from __future__ import annotations

import httpx
import numpy as np
import pytest

from src.api.landsat_lst_client import (
    AsyncLandsatLSTClient,
    calibrate_surface_temperature,
    landsat_clear_mask,
    spatial_surface_context_metrics,
    summarize_surface_temperature,
)


def test_qa_mask_and_calibration_do_not_double_scale():
    qa = np.array([0, 1 << 3, 1 << 4], dtype=np.uint16)
    assert landsat_clear_mask(qa).tolist() == [True, False, False]
    result = calibrate_surface_temperature(np.array([40000, 40000, 40000]), qa)
    assert result[0] == pytest.approx(12.5708)
    assert np.isnan(result[1:]).all()
    scaled = calibrate_surface_temperature(np.array([300.0]), np.array([0]), already_scaled=True)
    assert scaled[0] == pytest.approx(26.85)


def test_spatial_context_keeps_surface_air_gradient_distinct_from_error():
    result = spatial_surface_context_metrics([40, 42, 44, 46], [50, 53, 56, 60])
    assert result["spearman_rank_r"] == 1.0
    assert result["mean_surface_minus_air_c"] > 0
    assert "not forecast error" in result["interpretation"]


def test_surface_summary_uses_only_valid_pixels():
    result = summarize_surface_temperature(np.array([20.0, 30.0, np.nan]))
    assert result["valid_pixel_count"] == 2
    assert result["mean_surface_temperature_c"] == 25.0


@pytest.mark.asyncio
async def test_stac_search_keeps_surface_semantics_and_resolution_honest():
    def handler(request):
        if request.url.path.endswith("/collections/landsat-c2-l2"):
            return httpx.Response(200, json={"id": "landsat-c2-l2"})
        return httpx.Response(200, json={"features": [{
            "id": "LC09_TEST", "properties": {"datetime": "2024-07-01T18:00:00Z", "eo:cloud_cover": 3},
            "assets": {
                "lwir11": {"href": "https://asset/st.tif", "raster:bands": [{"scale": 0.00341802, "offset": 149}]},
                "qa_pixel": {"href": "https://asset/qa.tif"},
            },
        }]})

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        result = await AsyncLandsatLSTClient(http_client=http).search(
            [-112.1, 33.4, -112.0, 33.5], "2024-07-01/2024-07-31"
        )
    observation = result["observations"][0]
    assert observation["variable"] == "surface_temperature_c"
    assert "air" not in observation["variable"]
    assert observation["native_thermal_resolution_m"] == 100
    assert observation["output_grid_resolution_m"] == 30
    assert observation["requires_pixel_qa_mask"] is True
