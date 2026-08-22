"""
FastAPI Routes for Academic Literature, Scientific Provenance & alphaXiv Search
"""

from __future__ import annotations

import logging

import json
import os
import re
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query, HTTPException

from src.api.alphaxiv_client import AlphaXivClient
from src.db.database import db_manager
from src.db.models import AcademicPaperRecord

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/research", tags=["Academic Provenance & Research"])

def _get_corpus_path() -> Optional[str]:
    candidates = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "docs", "research", "alphaxiv_research_corpus.json"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "alphaxiv_research_corpus.json"),
        os.path.join(os.getcwd(), "docs", "research", "alphaxiv_research_corpus.json"),
        os.path.join(os.getcwd(), "src", "data", "alphaxiv_research_corpus.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


@router.get("/corpus")
async def get_research_corpus() -> Dict[str, Any]:
    """
    Returns the indexed academic research corpus categorized by domain, synchronized with SQLite/Supabase.
    """
    corpus_path = _get_corpus_path()
    base_corpus: Dict[str, Any] = {}
    if corpus_path and os.path.exists(corpus_path):
        try:
            with open(corpus_path, "r", encoding="utf-8") as f:
                base_corpus = json.load(f)
        except Exception as exc:
            logger.warning("Could not read local research corpus %s: %s", corpus_path, exc)

    # Query latest papers from SQLite / Supabase
    db_papers = await db_manager.get_academic_papers(limit=200)
    if db_papers and len(db_papers) > 0:
        for p in db_papers:
            cat = p.get("category", "general")
            if cat not in base_corpus:
                base_corpus[cat] = {
                    "title": cat.replace("_", " ").title(),
                    "papers": [],
                }
            existing_ids = [
                x.get("arxiv_id") or x.get("paper_id") or x.get("id")
                for x in base_corpus[cat].get("papers", [])
            ]
            p_id = p.get("arxiv_id") or p.get("paper_id")
            if p_id not in existing_ids:
                base_corpus[cat]["papers"].append(p)

    return base_corpus


@router.get("/db-papers")
async def get_db_papers_flat(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=100, ge=1, le=500),
) -> Dict[str, Any]:
    """
    Returns a flat list of academic papers queried directly from the SQLite / Supabase database.
    """
    papers = await db_manager.get_academic_papers(category=category, search=search, limit=limit)
    return {
        "total": len(papers),
        "source": "hybrid_database" if db_manager.is_supabase_enabled else "local_database",
        "papers": papers,
    }



def _search_persisted_corpus(
    stored: List[Dict[str, Any]], query: str, limit: int
) -> List[Dict[str, Any]]:
    """
    Rank previously persisted papers against a query by term overlap.

    Deliberately simple: this is a degraded path used when arXiv is unreachable
    or throttling, not a general search engine. Scores title matches above
    abstract matches so an exact-topic paper outranks a passing mention.
    """
    terms = [w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2]
    if not terms:
        return stored[:limit]

    scored = []
    for paper in stored:
        title = str(paper.get("title", "")).lower()
        abstract = str(paper.get("abstract", "")).lower()
        score = sum(3 for w in terms if w in title) + sum(1 for w in terms if w in abstract)
        if score:
            scored.append((score, paper))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [paper for _, paper in scored[:limit]]


@router.get("/search")
async def search_academic_papers(
    query: str = Query(..., description="Academic search query, e.g. 'cool pavement urban heat island'"),
    limit: int = Query(5, ge=1, le=20, description="Max papers to return"),
    sort_by: str = Query("relevance", enum=["relevance", "submittedDate", "lastUpdatedDate"]),
) -> Dict[str, Any]:
    """
    Live query to arXiv and alphaXiv API.
    Returns structured paper metadata and automatically persists newly discovered papers to database.
    """
    client = AlphaXivClient()
    try:
        papers = await client.search_papers(query=query, limit=limit, sort_by=sort_by)

        # Asynchronously persist newly found papers to SQLite / Supabase
        for p in papers:
            try:
                arxiv_id = p.get("arxiv_id") or p.get("id") or p.get("paper_id") or ""
                record = AcademicPaperRecord(
                    paper_id=f"arxiv:{arxiv_id}" if arxiv_id and not arxiv_id.startswith("arxiv:") else (arxiv_id or p.get("title", "")[:30]),
                    title=p.get("title", "Untitled"),
                    authors=p.get("authors", []),
                    year=int(p.get("year", 2024)),
                    category="live_search_discovery",
                    journal_or_venue=p.get("journal_or_venue") or p.get("venue"),
                    doi=p.get("doi"),
                    arxiv_id=arxiv_id,
                    alphaxiv_url=p.get("alphaxiv_url"),
                    pdf_url=p.get("pdf_url"),
                    abstract=p.get("abstract", ""),
                    latex_formula=p.get("latex_formula"),
                    key_findings=p.get("key_findings"),
                    relevance_to_fortyguard=p.get("relevance_to_fortyguard"),
                )
                await db_manager.save_academic_paper(record)
            except Exception as exc:
                logger.warning("Failed to persist academic paper: %s", exc, exc_info=True)

        source = "arxiv_live"

        # arXiv rate-limits aggressively (HTTP 429) and the client swallows the
        # failure into an empty list, so a throttled request previously rendered
        # the Academic Provenance tab blank. Every paper we have ever resolved is
        # already persisted, so fall back to that corpus instead of showing
        # nothing - and say which source answered.
        if not papers:
            papers = _search_persisted_corpus(await db_manager.get_academic_papers(limit=200), query, limit)
            source = "local_corpus" if papers else "unavailable"

        return {
            "query": query,
            "count": len(papers),
            "source": source,
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
