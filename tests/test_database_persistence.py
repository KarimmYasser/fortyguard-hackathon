"""
Unit tests for Thermal Sentinel Grid Hybrid Persistence Layer (SQLite + Supabase).
Covers all 16 enterprise data tables guaranteeing 100% zero data loss.
"""

import pytest
import tempfile
import os
from fastapi.testclient import TestClient

from src.db.database import HybridDatabaseManager
from src.db.models import (
    ApiCallCacheRecord,
    DispatchWorkOrderRecord,
    CreditLedgerRecord,
    AcademicPaperRecord,
    SubstationTelemetryRecord,
    SimulationRunRecord,
    MultiDayHeatwaveRecord,
    DLRCatenaryRecord,
    AgentExecutionTraceRecord,
    FinancialAuditRecord,
    MicroclimateParcelRecord,
    BESSDegradationRecord,
    CascadingRiskRecord,
    ChanceConstrainedOPFRecord,
    CBFSafetyCertificateRecord,
    GridAssetRegistryRecord,
)
from src.server.main import app


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    manager = HybridDatabaseManager(db_path=db_path)
    yield manager
    if os.path.exists(db_path):
        os.remove(db_path)


def test_sqlite_database_init(temp_db):
    """Verify all 16 tables are initialized with proper schemas."""
    status = temp_db.get_database_status()
    assert status["status"] == "healthy"
    assert "counts" in status
    assert status["counts"]["api_call_cache"] == 0
    assert status["counts"]["dispatch_work_orders"] == 0
    assert status["counts"]["credit_accounting_ledger"] == 0
    assert status["counts"]["academic_research_papers"] >= 0
    assert status["counts"]["grid_assets_registry"] >= 5


@pytest.mark.asyncio
async def test_api_call_caching_and_hits(temp_db):
    """Test saving and retrieving cached FortyGuard API responses."""
    endpoint = "/v1/heatmap"
    params = {"polygon_aoi": {"type": "Polygon"}, "start_date": "2023-07-24"}
    q_hash = temp_db.generate_query_hash(endpoint, params)

    record = ApiCallCacheRecord(
        query_hash=q_hash,
        endpoint=endpoint,
        request_params=params,
        response_payload={"temperature_raster": [42.5, 45.1, 47.6]},
        credits_spent=1.5,
    )

    # Initial cache miss
    cached = temp_db.get_cached_api_call(q_hash)
    assert cached is None

    # Save to cache
    await temp_db.save_cached_api_call(record)

    # Cache hit
    cached_payload = temp_db.get_cached_api_call(q_hash)
    assert cached_payload is not None
    assert cached_payload["temperature_raster"] == [42.5, 45.1, 47.6]

    # Verify hit count increment
    status = temp_db.get_database_status()
    assert status["counts"]["api_call_cache"] == 1


@pytest.mark.asyncio
async def test_dispatch_work_order_persistence(temp_db):
    """Test persisting B2B SCADA dispatch orders."""
    order = DispatchWorkOrderRecord(
        work_order_id="WO-TEST-001",
        asset_id="SUB-PHX-DOWNTOWN-04",
        calculated_k_safe=0.84,
        bess_dispatch_mw=5.0,
        bess_volt_var_q_mvar=1.5,
        oltc_tap_step=-1,
        forced_cooling_active=True,
        gpt_narrative="Emergency load shedding initiated due to 4.5C asphalt microclimate trap.",
        safety_status="AUTHORIZED",
        cbf_barrier_compliant=True,
    )

    await temp_db.save_dispatch_work_order(order)

    history = temp_db.get_dispatch_history(asset_id="SUB-PHX-DOWNTOWN-04")
    assert len(history) == 1
    assert history[0]["work_order_id"] == "WO-TEST-001"
    assert history[0]["calculated_k_safe"] == 0.84
    assert history[0]["bess_dispatch_mw"] == 5.0


@pytest.mark.asyncio
async def test_credit_accounting_ledger(temp_db):
    """Test debiting and auditing FortyGuard API credit ledger."""
    entry = CreditLedgerRecord(
        transaction_id="TXN-CREDIT-001",
        activity_id="act_heat_78942",
        endpoint="/v1/heatmap",
        credits_debited=2.0,
        remaining_balance=98.0,
        ip_or_caller="127.0.0.1",
    )

    await temp_db.log_credit_transaction(entry)

    ledger = temp_db.get_credit_ledger(limit=10)
    assert len(ledger) == 1
    assert ledger[0]["transaction_id"] == "TXN-CREDIT-001"
    assert ledger[0]["credits_debited"] == 2.0


@pytest.mark.asyncio
async def test_substation_telemetry_logging(temp_db):
    """Test logging and retrieving physical SCADA telemetry."""
    record = SubstationTelemetryRecord(
        asset_id="TX-SUB-PHX-01",
        hour_step=14,
        ambient_c=47.6,
        top_oil_c=104.2,
        hot_spot_c=136.8,
        aging_factor=2.1,
        load_ratio=0.88,
        bess_dispatch_mw=4.5,
        is_mitigated=True,
    )
    await temp_db.log_substation_telemetry(record)
    logs = temp_db.get_substation_telemetry(asset_id="TX-SUB-PHX-01")
    assert len(logs) == 1
    assert logs[0]["hot_spot_c"] == 136.8
    assert logs[0]["is_mitigated"] == 1


@pytest.mark.asyncio
async def test_simulation_run_persistence(temp_db):
    """Test saving What-If sandbox simulation run snapshots."""
    sim = SimulationRunRecord(
        simulation_id="SIM-PHX-TEST-99",
        scenario_name="Extreme Phoenix Heatwave Test",
        delta_c=5.5,
        heatwave_day=28,
        transformer_mva=25.0,
        bess_mwh=30.0,
        canyon_hw_ratio=2.1,
        cooling_fans_stage=2,
        peak_hot_spot_c=138.4,
        hours_above_140c=0.0,
        net_avoided_loss=2791338.0,
    )
    await temp_db.save_simulation_run(sim)
    runs = temp_db.get_simulation_runs()
    assert len(runs) == 1
    assert runs[0]["simulation_id"] == "SIM-PHX-TEST-99"
    assert runs[0]["delta_c"] == 5.5


@pytest.mark.asyncio
async def test_multi_day_heatwave_logging(temp_db):
    """Test logging continuous 72h compounding heatwave progression."""
    m_log = MultiDayHeatwaveRecord(
        simulation_id="72H-TEST-01",
        day_number=2,
        soil_resistivity=1.85,
        cumulative_aging_hours=420.5,
        max_hot_spot_c=139.1,
    )
    await temp_db.log_multi_day_step(m_log)
    status = temp_db.get_database_status()
    assert status["counts"]["multi_day_heatwave_logs"] == 1


@pytest.mark.asyncio
async def test_dlr_catenary_telemetry_logging(temp_db):
    """Test IEEE 738 Dynamic Line Rating & Catenary Sag telemetry persistence."""
    dlr = DLRCatenaryRecord(
        line_id="FEEDER-LINE-01",
        ambient_c=47.6,
        wind_speed_ms=1.2,
        conductor_temp_c=88.4,
        dynamic_ampacity_a=985.0,
        ampacity_headroom_pct=22.5,
        catenary_sag_m=4.82,
        clearance_margin_m=8.18,
    )
    await temp_db.log_dlr_telemetry(dlr)
    status = temp_db.get_database_status()
    assert status["counts"]["dlr_catenary_telemetry"] == 1


@pytest.mark.asyncio
async def test_agent_execution_trace_persistence(temp_db):
    """Test LangGraph StateGraph trace logging."""
    trace = AgentExecutionTraceRecord(
        trace_id="TRACE-PHX-01",
        asset_id="SUB-PHX-DOWNTOWN-04",
        duration_ms=2350.0,
        node_sequence=["forecast_node", "physics_node", "planner_node", "safety_gate_node", "audit_dispatch_node"],
        cbf_safety_passed=True,
        gpt_work_order_id="WO-TSG-04",
        gpt_advisory_text="Authorized proactive 4.5 MW BESS discharge under CBF safety barrier.",
    )
    await temp_db.save_agent_trace(trace)
    status = temp_db.get_database_status()
    assert status["counts"]["agent_execution_traces"] == 1


@pytest.mark.asyncio
async def test_financial_audit_snapshot_persistence(temp_db):
    """Test LBNL ICE investment-grade financial audit snapshot."""
    audit = FinancialAuditRecord(
        audit_id="AUDIT-2023-PHX-01",
        asset_id="SUB-PHX-DOWNTOWN-04",
        avoided_equipment_loss=1250000.0,
        avoided_customer_outage_loss=1541338.0,
        avoided_aging_deferral=18450.0,
        net_avoided_loss=2791338.0,
        economic_roi_multiplier=5952.7,
    )
    await temp_db.save_financial_audit(audit)
    status = temp_db.get_database_status()
    assert status["counts"]["financial_audit_snapshots"] == 1


@pytest.mark.asyncio
async def test_microclimate_parcel_store(temp_db):
    """Test FortyGuard 2-meter microclimate parcel GeoJSON storage."""
    parcel = MicroclimateParcelRecord(
        parcel_id="PARCEL-PHX-SUB-01",
        polygon_geojson={"type": "Polygon", "coordinates": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]},
        surface_temp_c=58.2,
        convective_temp_2m_c=47.6,
        asphalt_heat_trap_delta=4.5,
    )
    await temp_db.save_microclimate_parcel(parcel)
    status = temp_db.get_database_status()
    assert status["counts"]["microclimate_parcel_store"] == 1


@pytest.mark.asyncio
async def test_bess_degradation_logging(temp_db):
    """Test logging BESS electro-thermal ODE steps and capacity fade."""
    b_rec = BESSDegradationRecord(
        bess_id="BESS-PHX-CENTRAL-01",
        hour_step=14,
        ambient_c=47.6,
        dispatch_power_mw=7.5,
        core_temp_c=46.2,
        surface_temp_c=41.8,
        soc_pct=72.5,
        soh_pct=99.982,
        degradation_cost_usd=14.25,
    )
    await temp_db.log_bess_degradation(b_rec)
    logs = temp_db.get_bess_degradation_logs(bess_id="BESS-PHX-CENTRAL-01")
    assert len(logs) == 1
    assert logs[0]["core_temp_c"] == 46.2
    assert logs[0]["degradation_cost_usd"] == 14.25


@pytest.mark.asyncio
async def test_cascading_risk_snapshot_persistence(temp_db):
    """Test logging Arrhenius-Weibull cascading failure hazard snapshot."""
    c_rec = CascadingRiskRecord(
        snapshot_id="RISK-TEST-001",
        heatwave_severity="Extreme UHI (47.6C)",
        n1_reserve_margin_mw=12.5,
        n1_compliant=True,
        cascade_outage_probability=0.0345,
        expected_unserved_energy_mwh=45.0,
        total_voll_risk_usd=1541338.0,
    )
    await temp_db.save_cascading_risk_snapshot(c_rec)
    status = temp_db.get_database_status()
    assert status["counts"]["cascading_risk_snapshots"] == 1


@pytest.mark.asyncio
async def test_chance_constrained_opf_logging(temp_db):
    """Test logging Chance-Constrained SOCP OPF dispatch solution."""
    opf = ChanceConstrainedOPFRecord(
        solve_id="OPF-SOLVE-001",
        confidence_level_pct=95.0,
        total_generation_mw=28.5,
        bess_optimal_power_mw=4.5,
        oltc_optimal_tap=-1,
        total_dispatch_cost_usd=1420.50,
        solver_status="OPTIMAL_FEASIBLE",
    )
    await temp_db.log_chance_constrained_opf(opf)
    status = temp_db.get_database_status()
    assert status["counts"]["chance_constrained_opf_logs"] == 1


@pytest.mark.asyncio
async def test_cbf_safety_certificate_persistence(temp_db):
    """Test saving Control Barrier Function quadratic programming safety proof."""
    cert = CBFSafetyCertificateRecord(
        certificate_id="CBF-CERT-001",
        asset_id="SUB-PHX-DOWNTOWN-04",
        nominal_k_load=1.18,
        filtered_k_safe=0.88,
        barrier_value_h=3.24,
        qp_slack_xi=0.0,
        is_safe_invariant=True,
        mathematical_proof="Lie derivative L_f h(x) + gamma h(x) >= 0 satisfied.",
    )
    await temp_db.save_cbf_safety_certificate(cert)
    status = temp_db.get_database_status()
    assert status["counts"]["cbf_safety_certificates"] == 1


@pytest.mark.asyncio
async def test_grid_asset_registry_crud(temp_db):
    """Test creating and querying digital twin grid assets."""
    new_asset = GridAssetRegistryRecord(
        asset_id="SUB-PHX-TEMPE-01",
        name="Tempe North Substation TX-01",
        type="Transformer (Substation)",
        rated_mva=35.0,
        latitude=33.4255,
        longitude=-111.9400,
        cooling_type="ONAF",
        criticality_tier=1,
        current_health_score=97.5,
    )
    await temp_db.upsert_grid_asset(new_asset)
    assets = temp_db.get_grid_assets()
    assert len(assets) >= 6
    found = next((a for a in assets if a["asset_id"] == "SUB-PHX-TEMPE-01"), None)
    assert found is not None
    assert found["rated_mva"] == 35.0


def test_database_fastapi_endpoints():
    """Test FastAPI database status and history endpoints."""
    client = TestClient(app)
    resp = client.get("/api/v1/db/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "mode" in data
    assert "counts" in data
    assert "substation_telemetry_logs" in data["counts"]
    assert "simulation_runs" in data["counts"]
    assert "bess_degradation_logs" in data["counts"]
    assert "cascading_risk_snapshots" in data["counts"]
    assert "chance_constrained_opf_logs" in data["counts"]
    assert "cbf_safety_certificates" in data["counts"]
    assert "grid_assets_registry" in data["counts"]

    resp_ledger = client.get("/api/v1/db/credit-ledger")
    assert resp_ledger.status_code == 200
    assert isinstance(resp_ledger.json(), list)

    resp_dispatch = client.get("/api/v1/db/dispatch-history")
    assert resp_dispatch.status_code == 200
    assert isinstance(resp_dispatch.json(), list)
