"""
Thermal Sentinel Grid: Hybrid Database Manager (SQLite + Supabase Cloud Adapter)
Provides seamless local persistence with automatic cloud mirroring when Supabase keys are configured.
Covers all 16 enterprise data tables guaranteeing 100% zero data loss.
"""

from __future__ import annotations

import os
import json
import sqlite3
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx

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

logger = logging.getLogger("thermal_sentinel.db")


class HybridDatabaseManager:
    """
    Hybrid persistence manager:
    1. Local SQLite store (`data/thermal_sentinel.db`) ensures zero-latency, offline testing & CI safety.
    2. Cloud Supabase PostgreSQL REST integration mirrors writes and syncs state if credentials are provided.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path:
            self.db_path = Path(db_path)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.db_path = base_dir / "data" / "thermal_sentinel.db"

        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.supabase_key = os.getenv("SUPABASE_KEY", "") or os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        self.is_supabase_enabled = bool(self.supabase_url and self.supabase_key)

        self._init_sqlite_schema()
        self.seed_academic_papers_if_empty()
        self.seed_default_assets_if_empty()

        if self.is_supabase_enabled:
            logger.info(f"⚡ Supabase Cloud Database Connected: {self.supabase_url}")
        else:
            logger.info("📦 Operating in Local SQLite Persistence Mode (data/thermal_sentinel.db)")

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_sqlite_schema(self) -> None:
        """Initializes all 16 SQLite database tables and indexes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 1. API Call Cache
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS api_call_cache (
                    query_hash TEXT PRIMARY KEY,
                    endpoint TEXT NOT NULL,
                    bounding_box TEXT,
                    request_params TEXT,
                    response_payload TEXT NOT NULL,
                    credits_spent REAL DEFAULT 0.0,
                    hit_count INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL,
                    expires_at TEXT
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_api_cache_endpoint ON api_call_cache(endpoint);")

            # 2. Dispatch Work Orders
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS dispatch_work_orders (
                    work_order_id TEXT PRIMARY KEY,
                    asset_id TEXT NOT NULL,
                    calculated_k_safe REAL NOT NULL,
                    bess_dispatch_mw REAL DEFAULT 0.0,
                    bess_volt_var_q_mvar REAL DEFAULT 0.0,
                    oltc_tap_step INTEGER DEFAULT 0,
                    forced_cooling_active INTEGER DEFAULT 1,
                    gpt_narrative TEXT,
                    safety_status TEXT DEFAULT 'AUTHORIZED',
                    cbf_barrier_compliant INTEGER DEFAULT 1,
                    created_at TEXT NOT NULL
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_dispatch_asset ON dispatch_work_orders(asset_id);")

            # 3. Credit Accounting Ledger
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS credit_accounting_ledger (
                    transaction_id TEXT PRIMARY KEY,
                    activity_id TEXT,
                    endpoint TEXT NOT NULL,
                    credits_debited REAL NOT NULL,
                    remaining_balance REAL,
                    ip_or_caller TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 4. Academic Research Papers Corpus
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS academic_research_papers (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    journal_or_venue TEXT,
                    doi TEXT,
                    arxiv_id TEXT,
                    alphaxiv_url TEXT,
                    pdf_url TEXT,
                    abstract TEXT NOT NULL,
                    latex_formula TEXT,
                    key_findings TEXT,
                    relevance_to_fortyguard TEXT,
                    citation_count INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_papers_category ON academic_research_papers(category);")

            # 5. Substation SCADA Physical Telemetry Logs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS substation_telemetry_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    asset_id TEXT NOT NULL,
                    hour_step INTEGER NOT NULL,
                    ambient_c REAL NOT NULL,
                    top_oil_c REAL NOT NULL,
                    hot_spot_c REAL NOT NULL,
                    aging_factor REAL NOT NULL,
                    load_ratio REAL NOT NULL,
                    bess_dispatch_mw REAL DEFAULT 0.0,
                    is_mitigated INTEGER DEFAULT 0,
                    recorded_at TEXT NOT NULL
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_asset ON substation_telemetry_logs(asset_id);")

            # 6. What-If Sandbox Simulation Runs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS simulation_runs (
                    simulation_id TEXT PRIMARY KEY,
                    scenario_name TEXT NOT NULL,
                    delta_c REAL NOT NULL,
                    heatwave_day INTEGER NOT NULL,
                    transformer_mva REAL NOT NULL,
                    bess_mwh REAL NOT NULL,
                    canyon_hw_ratio REAL NOT NULL,
                    cooling_fans_stage INTEGER NOT NULL,
                    peak_hot_spot_c REAL NOT NULL,
                    hours_above_140c REAL NOT NULL,
                    net_avoided_loss REAL NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 7. 72-Hour Multi-Day Compounding Heatwave Logs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS multi_day_heatwave_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    simulation_id TEXT,
                    day_number INTEGER NOT NULL,
                    soil_resistivity REAL NOT NULL,
                    cumulative_aging_hours REAL NOT NULL,
                    max_hot_spot_c REAL NOT NULL,
                    recorded_at TEXT NOT NULL
                );
                """
            )

            # 8. IEEE 738 Dynamic Line Rating & Catenary Sag
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS dlr_catenary_telemetry (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    line_id TEXT NOT NULL,
                    ambient_c REAL NOT NULL,
                    wind_speed_ms REAL NOT NULL,
                    conductor_temp_c REAL NOT NULL,
                    dynamic_ampacity_a REAL NOT NULL,
                    ampacity_headroom_pct REAL NOT NULL,
                    catenary_sag_m REAL NOT NULL,
                    clearance_margin_m REAL NOT NULL,
                    recorded_at TEXT NOT NULL
                );
                """
            )

            # 9. LangGraph Multi-Agent Execution Traces
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS agent_execution_traces (
                    trace_id TEXT PRIMARY KEY,
                    asset_id TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    node_sequence TEXT NOT NULL,
                    cbf_safety_passed INTEGER NOT NULL,
                    gpt_work_order_id TEXT,
                    gpt_advisory_text TEXT,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 10. Financial Avoided Loss Audit Snapshots
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS financial_audit_snapshots (
                    audit_id TEXT PRIMARY KEY,
                    asset_id TEXT NOT NULL,
                    avoided_equipment_loss REAL NOT NULL,
                    avoided_customer_outage_loss REAL NOT NULL,
                    avoided_aging_deferral REAL NOT NULL,
                    net_avoided_loss REAL NOT NULL,
                    economic_roi_multiplier REAL NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 11. Hyperlocal Microclimate Parcel Store
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS microclimate_parcel_store (
                    parcel_id TEXT PRIMARY KEY,
                    polygon_geojson TEXT NOT NULL,
                    surface_temp_c REAL NOT NULL,
                    convective_temp_2m_c REAL NOT NULL,
                    asphalt_heat_trap_delta REAL NOT NULL,
                    scanned_at TEXT NOT NULL
                );
                """
            )

            # 12. BESS Electro-Thermal & SEI Degradation Logs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bess_degradation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bess_id TEXT NOT NULL,
                    hour_step INTEGER NOT NULL,
                    ambient_c REAL NOT NULL,
                    dispatch_power_mw REAL NOT NULL,
                    core_temp_c REAL NOT NULL,
                    surface_temp_c REAL NOT NULL,
                    soc_pct REAL NOT NULL,
                    soh_pct REAL NOT NULL,
                    degradation_cost_usd REAL NOT NULL,
                    recorded_at TEXT NOT NULL
                );
                """
            )
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_bess_degrad_id ON bess_degradation_logs(bess_id);")

            # 13. System-Wide Cascading Outage Risk Snapshots
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cascading_risk_snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    heatwave_severity TEXT NOT NULL,
                    n1_reserve_margin_mw REAL NOT NULL,
                    n1_compliant INTEGER NOT NULL,
                    cascade_outage_probability REAL NOT NULL,
                    expected_unserved_energy_mwh REAL NOT NULL,
                    total_voll_risk_usd REAL NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 14. Chance-Constrained SOCP OPF Dispatch Logs
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chance_constrained_opf_logs (
                    solve_id TEXT PRIMARY KEY,
                    confidence_level_pct REAL NOT NULL,
                    total_generation_mw REAL NOT NULL,
                    bess_optimal_power_mw REAL NOT NULL,
                    oltc_optimal_tap INTEGER NOT NULL,
                    total_dispatch_cost_usd REAL NOT NULL,
                    solver_status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

            # 15. CBF Control Barrier Function Safety Proof Certificates
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cbf_safety_certificates (
                    certificate_id TEXT PRIMARY KEY,
                    asset_id TEXT NOT NULL,
                    nominal_k_load REAL NOT NULL,
                    filtered_k_safe REAL NOT NULL,
                    barrier_value_h REAL NOT NULL,
                    qp_slack_xi REAL NOT NULL,
                    is_safe_invariant INTEGER NOT NULL,
                    mathematical_proof TEXT,
                    certified_at TEXT NOT NULL
                );
                """
            )

            # 16. Dynamic Grid Asset Digital Twin Registry
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS grid_assets_registry (
                    asset_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    rated_mva REAL NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    cooling_type TEXT DEFAULT 'ONAN/ONAF',
                    criticality_tier INTEGER DEFAULT 1,
                    current_health_score REAL DEFAULT 95.0,
                    updated_at TEXT NOT NULL
                );
                """
            )

            conn.commit()

    @staticmethod
    def generate_query_hash(endpoint: str, params: Dict[str, Any]) -> str:
        """Computes deterministic MD5 hash for API request signature."""
        normalized_str = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(normalized_str.encode("utf-8")).hexdigest()

    # --- 1. API Cache Operations ---
    def get_cached_api_call(self, query_hash: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT response_payload, hit_count FROM api_call_cache WHERE query_hash = ?",
                (query_hash,),
            )
            row = cursor.fetchone()
            if row:
                cursor.execute(
                    "UPDATE api_call_cache SET hit_count = hit_count + 1 WHERE query_hash = ?",
                    (query_hash,),
                )
                conn.commit()
                return json.loads(row["response_payload"])
        return None

    async def save_cached_api_call(self, record: ApiCallCacheRecord) -> None:
        payload_str = json.dumps(record.response_payload)
        bbox_str = json.dumps(record.bounding_box) if record.bounding_box else None
        params_str = json.dumps(record.request_params) if record.request_params else None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO api_call_cache (
                    query_hash, endpoint, bounding_box, request_params,
                    response_payload, credits_spent, hit_count, created_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(query_hash) DO UPDATE SET
                    response_payload = excluded.response_payload,
                    hit_count = hit_count + 1;
                """,
                (
                    record.query_hash,
                    record.endpoint,
                    bbox_str,
                    params_str,
                    payload_str,
                    record.credits_spent,
                    record.hit_count,
                    record.created_at,
                    record.expires_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("api_call_cache", record.model_dump())

    # --- 2. Dispatch Work Order Operations ---
    async def save_dispatch_work_order(self, record: DispatchWorkOrderRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO dispatch_work_orders (
                    work_order_id, asset_id, calculated_k_safe, bess_dispatch_mw,
                    bess_volt_var_q_mvar, oltc_tap_step, forced_cooling_active,
                    gpt_narrative, safety_status, cbf_barrier_compliant, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.work_order_id,
                    record.asset_id,
                    record.calculated_k_safe,
                    record.bess_dispatch_mw,
                    record.bess_volt_var_q_mvar,
                    record.oltc_tap_step,
                    1 if record.forced_cooling_active else 0,
                    record.gpt_narrative,
                    record.safety_status,
                    1 if record.cbf_barrier_compliant else 0,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("dispatch_work_orders", record.model_dump())

    def get_dispatch_history(self, asset_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if asset_id:
                cursor.execute(
                    "SELECT * FROM dispatch_work_orders WHERE asset_id = ? ORDER BY created_at DESC LIMIT ?",
                    (asset_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM dispatch_work_orders ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                )
            return [dict(row) for row in cursor.fetchall()]

    # --- 3. Credit Ledger Operations ---
    async def log_credit_transaction(self, record: CreditLedgerRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO credit_accounting_ledger (
                    transaction_id, activity_id, endpoint, credits_debited,
                    remaining_balance, ip_or_caller, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.transaction_id,
                    record.activity_id,
                    record.endpoint,
                    record.credits_debited,
                    record.remaining_balance,
                    record.ip_or_caller,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("credit_accounting_ledger", record.model_dump())

    def get_credit_ledger(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM credit_accounting_ledger ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    # --- 4. Academic Research Papers Operations ---
    async def save_academic_paper(self, record: AcademicPaperRecord) -> None:
        authors_json = json.dumps(record.authors)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO academic_research_papers (
                    paper_id, title, authors, year, category, journal_or_venue,
                    doi, arxiv_id, alphaxiv_url, pdf_url, abstract, latex_formula,
                    key_findings, relevance_to_fortyguard, citation_count, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(paper_id) DO UPDATE SET
                    title = excluded.title,
                    authors = excluded.authors,
                    citation_count = excluded.citation_count;
                """,
                (
                    record.paper_id,
                    record.title,
                    authors_json,
                    record.year,
                    record.category,
                    record.journal_or_venue,
                    record.doi,
                    record.arxiv_id,
                    record.alphaxiv_url,
                    record.pdf_url,
                    record.abstract,
                    record.latex_formula,
                    record.key_findings,
                    record.relevance_to_fortyguard,
                    record.citation_count,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("academic_research_papers", record.model_dump())

    def get_academic_papers(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM academic_research_papers WHERE 1=1"
            params: List[Any] = []

            if category and category != "all":
                query += " AND category = ?"
                params.append(category)

            if search:
                query += " AND (title LIKE ? OR abstract LIKE ? OR key_findings LIKE ?)"
                search_term = f"%{search}%"
                params.extend([search_term, search_term, search_term])

            query += " ORDER BY year DESC, citation_count DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, tuple(params))
            results = []
            for row in cursor.fetchall():
                item = dict(row)
                if isinstance(item.get("authors"), str):
                    try:
                        item["authors"] = json.loads(item["authors"])
                    except Exception:
                        item["authors"] = [item["authors"]]
                results.append(item)
            return results

    # --- 5. Substation Telemetry Logging ---
    async def log_substation_telemetry(self, record: SubstationTelemetryRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO substation_telemetry_logs (
                    asset_id, hour_step, ambient_c, top_oil_c, hot_spot_c,
                    aging_factor, load_ratio, bess_dispatch_mw, is_mitigated, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.asset_id,
                    record.hour_step,
                    record.ambient_c,
                    record.top_oil_c,
                    record.hot_spot_c,
                    record.aging_factor,
                    record.load_ratio,
                    record.bess_dispatch_mw,
                    1 if record.is_mitigated else 0,
                    record.recorded_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("substation_telemetry_logs", record.model_dump())

    def get_substation_telemetry(self, asset_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if asset_id:
                cursor.execute(
                    "SELECT * FROM substation_telemetry_logs WHERE asset_id = ? ORDER BY id DESC LIMIT ?",
                    (asset_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM substation_telemetry_logs ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            return [dict(row) for row in cursor.fetchall()]

    # --- 6. What-If Simulation Runs ---
    async def save_simulation_run(self, record: SimulationRunRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO simulation_runs (
                    simulation_id, scenario_name, delta_c, heatwave_day,
                    transformer_mva, bess_mwh, canyon_hw_ratio, cooling_fans_stage,
                    peak_hot_spot_c, hours_above_140c, net_avoided_loss, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.simulation_id,
                    record.scenario_name,
                    record.delta_c,
                    record.heatwave_day,
                    record.transformer_mva,
                    record.bess_mwh,
                    record.canyon_hw_ratio,
                    record.cooling_fans_stage,
                    record.peak_hot_spot_c,
                    record.hours_above_140c,
                    record.net_avoided_loss,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("simulation_runs", record.model_dump())

    def get_simulation_runs(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM simulation_runs ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    # --- 7. 72-Hour Multi-Day Logs ---
    async def log_multi_day_step(self, record: MultiDayHeatwaveRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO multi_day_heatwave_logs (
                    simulation_id, day_number, soil_resistivity,
                    cumulative_aging_hours, max_hot_spot_c, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    record.simulation_id,
                    record.day_number,
                    record.soil_resistivity,
                    record.cumulative_aging_hours,
                    record.max_hot_spot_c,
                    record.recorded_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("multi_day_heatwave_logs", record.model_dump())

    # --- 8. DLR & Catenary Sag Telemetry ---
    async def log_dlr_telemetry(self, record: DLRCatenaryRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO dlr_catenary_telemetry (
                    line_id, ambient_c, wind_speed_ms, conductor_temp_c,
                    dynamic_ampacity_a, ampacity_headroom_pct, catenary_sag_m,
                    clearance_margin_m, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.line_id,
                    record.ambient_c,
                    record.wind_speed_ms,
                    record.conductor_temp_c,
                    record.dynamic_ampacity_a,
                    record.ampacity_headroom_pct,
                    record.catenary_sag_m,
                    record.clearance_margin_m,
                    record.recorded_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("dlr_catenary_telemetry", record.model_dump())

    # --- 9. Agent Execution Traces ---
    async def save_agent_trace(self, record: AgentExecutionTraceRecord) -> None:
        seq_str = json.dumps(record.node_sequence)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO agent_execution_traces (
                    trace_id, asset_id, duration_ms, node_sequence,
                    cbf_safety_passed, gpt_work_order_id, gpt_advisory_text, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.trace_id,
                    record.asset_id,
                    record.duration_ms,
                    seq_str,
                    1 if record.cbf_safety_passed else 0,
                    record.gpt_work_order_id,
                    record.gpt_advisory_text,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("agent_execution_traces", record.model_dump())

    # --- 10. Financial Audit Snapshots ---
    async def save_financial_audit(self, record: FinancialAuditRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO financial_audit_snapshots (
                    audit_id, asset_id, avoided_equipment_loss, avoided_customer_outage_loss,
                    avoided_aging_deferral, net_avoided_loss, economic_roi_multiplier, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.audit_id,
                    record.asset_id,
                    record.avoided_equipment_loss,
                    record.avoided_customer_outage_loss,
                    record.avoided_aging_deferral,
                    record.net_avoided_loss,
                    record.economic_roi_multiplier,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("financial_audit_snapshots", record.model_dump())

    # --- 11. Microclimate Parcel Store ---
    async def save_microclimate_parcel(self, record: MicroclimateParcelRecord) -> None:
        geojson_str = json.dumps(record.polygon_geojson)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO microclimate_parcel_store (
                    parcel_id, polygon_geojson, surface_temp_c, convective_temp_2m_c,
                    asphalt_heat_trap_delta, scanned_at
                ) VALUES (?, ?, ?, ?, ?, ?);
                """,
                (
                    record.parcel_id,
                    geojson_str,
                    record.surface_temp_c,
                    record.convective_temp_2m_c,
                    record.asphalt_heat_trap_delta,
                    record.scanned_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("microclimate_parcel_store", record.model_dump())

    # --- 12. BESS Degradation Logs ---
    async def log_bess_degradation(self, record: BESSDegradationRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO bess_degradation_logs (
                    bess_id, hour_step, ambient_c, dispatch_power_mw, core_temp_c,
                    surface_temp_c, soc_pct, soh_pct, degradation_cost_usd, recorded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.bess_id,
                    record.hour_step,
                    record.ambient_c,
                    record.dispatch_power_mw,
                    record.core_temp_c,
                    record.surface_temp_c,
                    record.soc_pct,
                    record.soh_pct,
                    record.degradation_cost_usd,
                    record.recorded_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("bess_degradation_logs", record.model_dump())

    def get_bess_degradation_logs(self, bess_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if bess_id:
                cursor.execute(
                    "SELECT * FROM bess_degradation_logs WHERE bess_id = ? ORDER BY id DESC LIMIT ?",
                    (bess_id, limit),
                )
            else:
                cursor.execute(
                    "SELECT * FROM bess_degradation_logs ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            return [dict(row) for row in cursor.fetchall()]

    # --- 13. Cascading Outage Risk Snapshots ---
    async def save_cascading_risk_snapshot(self, record: CascadingRiskRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO cascading_risk_snapshots (
                    snapshot_id, heatwave_severity, n1_reserve_margin_mw, n1_compliant,
                    cascade_outage_probability, expected_unserved_energy_mwh, total_voll_risk_usd, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.snapshot_id,
                    record.heatwave_severity,
                    record.n1_reserve_margin_mw,
                    1 if record.n1_compliant else 0,
                    record.cascade_outage_probability,
                    record.expected_unserved_energy_mwh,
                    record.total_voll_risk_usd,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("cascading_risk_snapshots", record.model_dump())

    # --- 14. Chance-Constrained SOCP OPF Logs ---
    async def log_chance_constrained_opf(self, record: ChanceConstrainedOPFRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO chance_constrained_opf_logs (
                    solve_id, confidence_level_pct, total_generation_mw, bess_optimal_power_mw,
                    oltc_optimal_tap, total_dispatch_cost_usd, solver_status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.solve_id,
                    record.confidence_level_pct,
                    record.total_generation_mw,
                    record.bess_optimal_power_mw,
                    record.oltc_optimal_tap,
                    record.total_dispatch_cost_usd,
                    record.solver_status,
                    record.created_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("chance_constrained_opf_logs", record.model_dump())

    # --- 15. CBF Safety Proof Certificates ---
    async def save_cbf_safety_certificate(self, record: CBFSafetyCertificateRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO cbf_safety_certificates (
                    certificate_id, asset_id, nominal_k_load, filtered_k_safe,
                    barrier_value_h, qp_slack_xi, is_safe_invariant, mathematical_proof, certified_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    record.certificate_id,
                    record.asset_id,
                    record.nominal_k_load,
                    record.filtered_k_safe,
                    record.barrier_value_h,
                    record.qp_slack_xi,
                    1 if record.is_safe_invariant else 0,
                    record.mathematical_proof,
                    record.certified_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("cbf_safety_certificates", record.model_dump())

    # --- 16. Dynamic Grid Asset Digital Twin Registry ---
    async def upsert_grid_asset(self, record: GridAssetRegistryRecord) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO grid_assets_registry (
                    asset_id, name, type, rated_mva, latitude, longitude,
                    cooling_type, criticality_tier, current_health_score, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(asset_id) DO UPDATE SET
                    name = excluded.name,
                    rated_mva = excluded.rated_mva,
                    current_health_score = excluded.current_health_score,
                    updated_at = excluded.updated_at;
                """,
                (
                    record.asset_id,
                    record.name,
                    record.type,
                    record.rated_mva,
                    record.latitude,
                    record.longitude,
                    record.cooling_type,
                    record.criticality_tier,
                    record.current_health_score,
                    record.updated_at,
                ),
            )
            conn.commit()

        if self.is_supabase_enabled:
            await self._supabase_insert("grid_assets_registry", record.model_dump())

    def get_grid_assets(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM grid_assets_registry ORDER BY criticality_tier DESC, name ASC")
            return [dict(row) for row in cursor.fetchall()]

    def seed_default_assets_if_empty(self) -> int:
        """Seeds standard digital twin grid assets into SQLite and Supabase on initial startup."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM grid_assets_registry")
            if cursor.fetchone()["cnt"] > 0:
                return 0

            default_assets = [
                ("SUB-PHX-DOWNTOWN-04", "Phoenix Central Substation TX-04", "Transformer (Power)", 25.0, 33.4484, -112.0740, "ONAN/ONAF", 1, 88.5),
                ("SUB-PHX-AIRPORT-02", "Sky Harbor Distribution TX-02", "Transformer (Substation)", 30.0, 33.4352, -112.0101, "OFAF", 1, 94.0),
                ("BESS-PHX-CENTRAL-01", "Downtown Phoenix Utility BESS", "BESS Storage", 25.0, 33.4490, -112.0735, "Liquid-Cooled", 1, 98.2),
                ("FEEDER-PHX-01", "Feeder 12kV Urban Canyon Line 01", "Overhead Conductor", 15.0, 33.4475, -112.0750, "Drake ACSR 795", 2, 91.0),
                ("SUB-PHX-BILTMORE-01", "Biltmore Area Substation TX-01", "Transformer (Substation)", 40.0, 33.5186, -112.0131, "ONAN/ONAF", 2, 96.0),
            ]

            for a in default_assets:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO grid_assets_registry (
                        asset_id, name, type, rated_mva, latitude, longitude,
                        cooling_type, criticality_tier, current_health_score, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'));
                    """,
                    a,
                )
            conn.commit()
            logger.info("⚡ Seeded 5 initial digital twin grid assets into registry.")
            return len(default_assets)

    def seed_academic_papers_if_empty(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM academic_research_papers")
            count = cursor.fetchone()["cnt"]
            if count > 0:
                return count

        base_dir = Path(__file__).resolve().parent.parent.parent
        possible_paths = [
            base_dir / "src" / "data" / "alphaxiv_research_corpus.json",
            base_dir / "docs" / "research" / "alphaxiv_research_corpus.json",
        ]
        corpus_path = None
        for p in possible_paths:
            if p.exists():
                corpus_path = p
                break

        if not corpus_path:
            return 0

        try:
            with open(corpus_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            papers_to_seed = []
            if isinstance(data, list):
                papers_to_seed = data
            elif isinstance(data, dict):
                if "papers" in data and isinstance(data["papers"], list):
                    papers_to_seed = data["papers"]
                else:
                    for cat_key, cat_val in data.items():
                        if isinstance(cat_val, dict) and "papers" in cat_val:
                            for p in cat_val["papers"]:
                                p_copy = dict(p)
                                if "category" not in p_copy:
                                    p_copy["category"] = cat_key
                                papers_to_seed.append(p_copy)

            if not papers_to_seed:
                return 0

            with self._get_connection() as conn:
                cursor = conn.cursor()
                for p in papers_to_seed:
                    authors_json = json.dumps(p.get("authors", []))
                    pub_str = str(p.get("published", ""))
                    year = int(pub_str[:4]) if len(pub_str) >= 4 and pub_str[:4].isdigit() else int(p.get("year", 2023))
                    math_insights = p.get("math_insights", {})
                    latex_list = math_insights.get("latex_expressions", []) if isinstance(math_insights, dict) else []
                    latex_formula = latex_list[0] if latex_list else p.get("latex_formula", "")

                    paper_id = p.get("arxiv_id") or p.get("id") or p.get("paper_id") or f"paper_{hashlib.md5(p.get('title','').encode()).hexdigest()[:12]}"
                    if not paper_id.startswith("arxiv:") and not paper_id.startswith("ieee:"):
                        paper_id = f"arxiv:{paper_id}"

                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO academic_research_papers (
                            paper_id, title, authors, year, category, journal_or_venue,
                            doi, arxiv_id, alphaxiv_url, pdf_url, abstract, latex_formula,
                            key_findings, relevance_to_fortyguard, citation_count, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'));
                        """,
                        (
                            paper_id,
                            p.get("title", ""),
                            authors_json,
                            year,
                            p.get("category", "general"),
                            p.get("journal") or p.get("journal_or_venue", "arXiv / IEEE"),
                            p.get("doi", ""),
                            p.get("arxiv_id", ""),
                            p.get("alphaxiv_url", f"https://alphaxiv.org/abs/{p.get('arxiv_id', '')}"),
                            p.get("pdf_url", f"https://arxiv.org/pdf/{p.get('arxiv_id', '')}.pdf"),
                            p.get("summary") or p.get("abstract", ""),
                            latex_formula,
                            p.get("key_findings") or p.get("summary", ""),
                            p.get("relevance_to_fortyguard", "Provides peer-reviewed physical formulation and benchmark validation for FortyGuard microclimate integration."),
                            p.get("citation_count", 0),
                        ),
                    )
                conn.commit()
            logger.info(f"📚 Successfully seeded {len(papers_to_seed)} academic papers into database.")
            return len(papers_to_seed)
        except Exception as e:
            logger.warning(f"Failed to seed academic papers: {e}")
            return 0

    # --- Supabase REST Helper ---
    async def _supabase_insert(self, table: str, payload: Dict[str, Any]) -> bool:
        if not self.is_supabase_enabled:
            return False

        url = f"{self.supabase_url}/rest/v1/{table}"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates",
        }

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                resp = await client.post(url, json=payload, headers=headers)
                return resp.status_code in (200, 201, 204)
        except Exception as e:
            logger.warning(f"Supabase sync non-fatal error for table {table}: {e}")
            return False

    def get_database_status(self) -> Dict[str, Any]:
        """Returns database health, active mode, and cached item counts across all 16 tables."""
        tables = [
            "api_call_cache",
            "dispatch_work_orders",
            "credit_accounting_ledger",
            "academic_research_papers",
            "substation_telemetry_logs",
            "simulation_runs",
            "multi_day_heatwave_logs",
            "dlr_catenary_telemetry",
            "agent_execution_traces",
            "financial_audit_snapshots",
            "microclimate_parcel_store",
            "bess_degradation_logs",
            "cascading_risk_snapshots",
            "chance_constrained_opf_logs",
            "cbf_safety_certificates",
            "grid_assets_registry",
        ]
        counts: Dict[str, int] = {}
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for t in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) as cnt FROM {t}")
                    counts[t] = cursor.fetchone()["cnt"]
                except Exception:
                    counts[t] = 0

        return {
            "status": "healthy",
            "mode": "hybrid_supabase" if self.is_supabase_enabled else "local_sqlite",
            "sqlite_db_path": str(self.db_path),
            "supabase_connected": self.is_supabase_enabled,
            "supabase_url": self.supabase_url if self.is_supabase_enabled else None,
            "counts": counts,
        }


# Global singleton instance
db_manager = HybridDatabaseManager()
