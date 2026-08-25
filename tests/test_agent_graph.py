import pytest
from src.agent.graph import create_thermal_sentinel_graph, run_thermal_sentinel_agent


@pytest.mark.asyncio
async def test_langgraph_workflow_execution():
    graph = create_thermal_sentinel_graph()
    assert graph is not None

    result = await run_thermal_sentinel_agent(
        target_city="Phoenix, AZ",
        asset_id="SUB-PHX-DOWNTOWN-04",
        asset_name="Phoenix Central Substation TX-04",
    )

    assert "fortyguard_forecast" in result
    assert len(result["fortyguard_forecast"]) == 12
    assert "baseline_trajectory" in result
    assert "mitigated_trajectory" in result
    assert "safety_gate_verdict" in result
    assert "economic_evaluation" in result
    assert "b2b_work_order" in result
    assert "b2c_advisory" in result
    assert len(result["audit_trail"]) >= 5

    # Check that safety gate capped the peak hot spot below 140°C
    mitigated = result["mitigated_trajectory"]
    assert mitigated["peak_hot_spot_c"] < 140.0

    # Check economic ROI
    eco = result["economic_evaluation"]
    assert eco["net_avoided_loss_usd"] > 100000.0
    assert eco["roi_multiple"] > 15.0

    # Check structured "Fact vs. Finding" Decision Object
    assert "defensible_finding" in result
    finding = result["defensible_finding"]
    assert finding["asset_id"] == "SUB-PHX-DOWNTOWN-04"
    assert "raw_fact" in finding
    assert finding["continuous_persistence_hours"] >= 10.0
    assert finding["arrhenius_aging_acceleration"] > 1.0
    assert "causality_explanation" in finding
    assert "defensible_narrative" in finding
    assert finding["net_avoided_loss_usd"] > 0

