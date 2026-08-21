"""
Database module for Thermal Sentinel Grid.
Exports Hybrid Database Manager, all 16 models, and singleton instance.
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
