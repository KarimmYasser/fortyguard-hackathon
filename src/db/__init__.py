"""
Database module for Thermal Sentinel Grid.
Exports the hybrid database manager and singleton instance for all 17 application tables.
"""

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
from src.db.database import HybridDatabaseManager, db_manager

__all__ = [
    "ApiCallCacheRecord",
    "DispatchWorkOrderRecord",
    "CreditLedgerRecord",
    "AcademicPaperRecord",
    "SubstationTelemetryRecord",
    "SimulationRunRecord",
    "MultiDayHeatwaveRecord",
    "DLRCatenaryRecord",
    "AgentExecutionTraceRecord",
    "FinancialAuditRecord",
    "MicroclimateParcelRecord",
    "BESSDegradationRecord",
    "CascadingRiskRecord",
    "ChanceConstrainedOPFRecord",
    "CBFSafetyCertificateRecord",
    "GridAssetRegistryRecord",
    "HybridDatabaseManager",
    "db_manager",
]
