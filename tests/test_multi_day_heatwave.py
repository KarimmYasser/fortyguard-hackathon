import pytest
from src.physics.multi_day_heatwave import MultiDayHeatwaveEngine


def test_72h_multi_day_compounding_simulation():
    engine = MultiDayHeatwaveEngine()
    result = engine.run_72h_simulation()

    assert result.total_hours == 72
    assert len(result.days_summary) == 3
    assert len(result.timeline_72h) == 72

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
