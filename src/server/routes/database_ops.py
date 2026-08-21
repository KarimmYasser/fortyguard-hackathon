"""
Database Operations & Ledger Inspection Router
Exposes database status, credit accounting ledger, and dispatch history.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query

from src.db.database import db_manager

router = APIRouter(prefix="/db", tags=["Database & Cloud Persistence"])


@router.get("/status")
async def get_db_status() -> Dict[str, Any]:
    """
    Returns persistence mode (Local SQLite vs Supabase PostgreSQL) and active table counts.
    """
    return await db_manager.get_database_status()


@router.get("/credit-ledger")
async def get_credit_ledger_entries(limit: int = Query(default=50, ge=1, le=500)) -> List[Dict[str, Any]]:
    """
    Returns recent FortyGuard API credit expenditures and remaining balance ledger.
    """
    return await db_manager.get_credit_ledger(limit=limit)


@router.get("/dispatch-history")
async def get_dispatch_history_entries(
    asset_id: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=500),
) -> List[Dict[str, Any]]:
    """
    Returns historical B2B SCADA work orders authorized by the multi-agent system.
    """
    return await db_manager.get_dispatch_history(asset_id=asset_id, limit=limit)
