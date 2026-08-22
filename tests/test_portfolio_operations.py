from fastapi.testclient import TestClient

from src.operations.portfolio import (
    build_mitigation_evidence,
    calculate_worker_windows,
    load_default_environment_profile,
    rank_portfolio,
)
from src.server.main import app


def test_worker_screen_uses_measured_fields_without_claiming_wbgt_compliance():
    profile, _ = load_default_environment_profile()
    screen = calculate_worker_windows(profile)

    assert screen["classification"] == "derived_operational_screen"
    assert screen["occupational_safety_certification"] is False
    assert "no globe-temperature" in screen["limitations"]
    assert screen["windows"]
    assert all(row["air_temp_2m_c"] is not None for row in screen["hourly_screen"])
    assert all(row["wet_bulb_temp_c"] is not None for row in screen["hourly_screen"])


def test_portfolio_ranking_is_deterministic_and_tie_broken_by_asset_id():
    profile, _ = load_default_environment_profile()
    assets = [
        {
            "asset_id": "B",
            "name": "B",
            "type": "Transformer",
            "current_load_percentage": 90.0,
            "current_health_score": 80.0,
            "criticality_tier": 1,
            "max_safe_ambient_temp_c": 40.0,
        },
        {
            "asset_id": "A",
            "name": "A",
            "type": "Transformer",
            "current_load_percentage": 90.0,
            "current_health_score": 80.0,
            "criticality_tier": 1,
            "max_safe_ambient_temp_c": 40.0,
        },
    ]

    ranked = rank_portfolio(assets, profile)
    assert [row["asset_id"] for row in ranked] == ["A", "B"]
    assert ranked[0]["risk_score"] == ranked[1]["risk_score"]
    assert ranked[0]["rank"] == 1


def test_evidence_digest_is_stable_even_though_generation_time_changes():
    profile, metadata = load_default_environment_profile()
    screen = calculate_worker_windows(profile)
    rankings = rank_portfolio([], profile, worker_screen=screen)

    first = build_mitigation_evidence(rankings, screen, metadata)
    second = build_mitigation_evidence(rankings, screen, metadata)

    assert first["evidence_id"] == second["evidence_id"]
    assert first["sha256"] == second["sha256"]
    assert first["read_only"] is True


def test_operations_and_mcp_endpoints_share_deterministic_core():
    client = TestClient(app)
    portfolio = client.get("/api/v1/operations/portfolio")
    assert portfolio.status_code == 200
    payload = portfolio.json()
    assert payload["portfolio"]["asset_count"] >= 3
    assert payload["mitigation_evidence"]["immutable_input_digest"] is True

    tools = client.post("/api/v1/mcp", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {},
    })
    assert tools.status_code == 200
    assert {tool["name"] for tool in tools.json()["result"]["tools"]} == {
        "rank_portfolio_risk",
        "find_worker_intervention_windows",
        "get_mitigation_evidence",
    }

    call = client.post("/api/v1/mcp", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_mitigation_evidence", "arguments": {}},
    })
    assert call.status_code == 200
    mcp_evidence = call.json()["result"]["structuredContent"]
    assert mcp_evidence["evidence_id"] == payload["mitigation_evidence"]["evidence_id"]
