from src.physics.multi_day_heatwave import MultiDayHeatwaveEngine


def test_72h_multi_day_compounding_simulation():
    engine = MultiDayHeatwaveEngine()
    result = engine.run_72h_simulation()

    assert result.total_hours == 72
    assert len(result.days_summary) == 3
    assert len(result.timeline_72h) == 72
    assert [step["global_hour"] for step in result.timeline_72h] == list(range(72))
    assert {step["boundary_data_source"] for step in result.timeline_72h} == {"fortyguard_live"}
    assert result.scenario_metadata["provenance"]["data_source"] == "fortyguard_live_capture"

    # The environmental forcing is the captured 24x3 profile, not the retired
    # airport-plus-delta sinusoid. These peaks come directly from the fixture.
    assert [day.date for day in result.days_summary] == [
        "2023-07-24",
        "2023-07-25",
        "2023-07-26",
    ]
    assert [day.peak_ambient_2m_c for day in result.days_summary] == [42.44, 42.76, 42.52]
    assert all("airport_temp_c" not in step for step in result.timeline_72h)

    # Spatial spread must be the measured spread at the daily peak hour, not
    # max(ambient) - min(coolest) across different hours.
    for day in result.days_summary:
        assert round(day.peak_ambient_2m_c - day.coolest_tile_at_peak_c, 2) == day.intra_aoi_spread_c

    # Verify compounding soil dryout progression
    d1 = result.days_summary[0]
    d2 = result.days_summary[1]
    d3 = result.days_summary[2]

    # Soil resistivity must surge monotonically across days
    assert d1.end_of_day_soil_resistivity_rho < d2.end_of_day_soil_resistivity_rho
    assert d2.end_of_day_soil_resistivity_rho < d3.end_of_day_soil_resistivity_rho
    assert d3.end_of_day_soil_resistivity_rho >= 2.40

    # Total loss of life avoided must be substantial (>1000 hours)
    assert result.total_avoided_loss_of_life_hours > 1000.0
    assert result.cumulative_net_avoided_loss_usd > 2500000.0
