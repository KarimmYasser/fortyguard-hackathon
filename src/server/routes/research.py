"""
FastAPI Routes for Academic Literature, Scientific Provenance & alphaXiv Search
"""

from __future__ import annotations

import json
import os
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query, HTTPException

from src.api.alphaxiv_client import AlphaXivClient

router = APIRouter(prefix="/api/v1/research", tags=["Academic Provenance & Research"])

CORPUS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "docs",
    "research",
    "alphaxiv_research_corpus.json",
)


@router.get("/corpus")
async def get_research_corpus() -> Dict[str, Any]:
    """
    Returns the indexed academic research corpus (47 peer-reviewed papers & preprints)
    grounding the Thermal Sentinel Grid physics, cool pavements, and satellite super-resolution models.
    """
    if os.path.exists(CORPUS_PATH):
        try:
            with open(CORPUS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read research corpus: {e}")

    # Fallback if file not found at relative path
    client = AlphaXivClient()
    return {
        "physics_informed_thermal_pdes": {
            "title": "Physics-Informed Neural Networks (PINNs) & Thermal PDEs",
            "papers": [],
        }
    }


@router.get("/search")
async def search_academic_papers(
    query: str = Query(..., description="Academic search query, e.g. 'cool pavement urban heat island'"),
    limit: int = Query(5, ge=1, le=20, description="Max papers to return"),
    sort_by: str = Query("relevance", enum=["relevance", "submittedDate", "lastUpdatedDate"]),
) -> Dict[str, Any]:
    """
    Live query to arXiv and alphaXiv API.
    Returns structured paper metadata, mathematical insights, and IEEE/BibTeX citations.
    """
    client = AlphaXivClient()
    try:
        papers = await client.search_papers(query=query, limit=limit, sort_by=sort_by)
        return {
            "query": query,
            "count": len(papers),
            "papers": papers,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Academic search failed: {e}")


@router.get("/paper/{arxiv_id}")
async def get_paper_metadata(arxiv_id: str) -> Dict[str, Any]:
    """
    Fetches detailed paper metadata and alphaXiv discussion link by arXiv ID.
    """
    client = AlphaXivClient()
    paper = await client.get_paper_details(arxiv_id)
    if not paper:
        raise HTTPException(status_code=404, detail=f"Paper '{arxiv_id}' not found on arXiv/alphaXiv")
    return paper
