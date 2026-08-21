"""
alphaXiv & arXiv API Client - Scientific Paper Fetcher & Academic Provenance Adapter
Allows Thermal Sentinel Grid agents to dynamically search arXiv / alphaXiv papers, retrieve
mathematical models, extract formulas, and generate verified academic citations.
"""

import os
import re
import logging
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("thermal_sentinel.alphaxiv")

class AlphaXivClient:
    """
    Client for interacting with alphaXiv (https://alphaxiv.org) and arXiv API.
    Provides automated paper discovery, metadata extraction, mathematical parsing,
    and citation generation for urban thermal resilience modeling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.alphaxiv.org/v1",
        arxiv_api_url: str = "https://export.arxiv.org/api/query",
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.getenv("ALPHAXIV_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.arxiv_api_url = arxiv_api_url
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ThermalSentinelGrid/1.0 (academic-research-bot)",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def search_papers(
        self,
        query: str,
        limit: int = 5,
        sort_by: str = "relevance",
    ) -> List[Dict[str, Any]]:
        """
        Search arXiv / alphaXiv for papers matching a query.
        Uses arXiv Export API as robust ground truth with alphaXiv integration.
        """
        # Try alphaXiv API first if API key is present
        if self.api_key:
            try:
                url = f"{self.base_url}/search"
                params = {"q": query, "limit": limit}
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, headers=self._get_headers(), params=params)
                    if response.status_code == 200:
                        results = response.json().get("results", [])
                        if results:
                            return results
            except Exception as e:
                logger.warning("alphaXiv direct search failed, falling back to arXiv: %s", e)

        # Fallback to arXiv API with rich parsing
        return await self._search_arxiv(query, limit, sort_by)

    async def _search_arxiv(
        self,
        query: str,
        limit: int = 5,
        sort_by: str = "relevance",
    ) -> List[Dict[str, Any]]:
        """Query arXiv Atom API and parse structured metadata."""
        sort_map = {
            "relevance": "relevance",
            "submittedDate": "submittedDate",
            "lastUpdatedDate": "lastUpdatedDate",
        }
        arxiv_sort = sort_map.get(sort_by, "relevance")
        
        # Format query for arXiv API
        formatted_query = query.replace(" ", "+")
        url = f"{self.arxiv_api_url}?search_query=all:{formatted_query}&start=0&max_results={limit}&sortBy={arxiv_sort}&sortOrder=descending"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code != 200:
                    logger.error("arXiv API returned HTTP %d: %s", response.status_code, response.text)
                    return []

                root = ET.fromstring(response.text)
                namespace = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
                
                results = []
                for entry in root.findall("atom:entry", namespace):
                    id_elem = entry.find("atom:id", namespace)
                    raw_id = id_elem.text.strip() if id_elem is not None else ""
                    arxiv_id = raw_id.split("/abs/")[-1] if "/abs/" in raw_id else raw_id

                    title_elem = entry.find("atom:title", namespace)
                    title = " ".join(title_elem.text.split()) if title_elem is not None else "Untitled"

                    summary_elem = entry.find("atom:summary", namespace)
                    summary = " ".join(summary_elem.text.split()) if summary_elem is not None else ""

                    published_elem = entry.find("atom:published", namespace)
                    published = published_elem.text.strip() if published_elem is not None else ""

                    updated_elem = entry.find("atom:updated", namespace)
                    updated = updated_elem.text.strip() if updated_elem is not None else ""

                    authors = []
                    for author in entry.findall("atom:author", namespace):
                        name = author.find("atom:name", namespace)
                        if name is not None and name.text:
                            authors.append(name.text.strip())

                    categories = []
                    for cat in entry.findall("atom:category", namespace):
                        term = cat.get("term")
                        if term:
                            categories.append(term)

                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    abs_url = f"https://arxiv.org/abs/{arxiv_id}"
                    alphaxiv_url = f"https://alphaxiv.org/abs/{arxiv_id}"

                    # Extract mathematical concepts and keywords
                    math_insights = self._extract_math_concepts(summary)

                    results.append({
                        "arxiv_id": arxiv_id,
                        "title": title,
                        "authors": authors,
                        "summary": summary,
                        "published": published,
                        "updated": updated,
                        "categories": categories,
                        "primary_category": categories[0] if categories else "cs.LG",
                        "pdf_url": pdf_url,
                        "arxiv_url": abs_url,
                        "alphaxiv_url": alphaxiv_url,
                        "math_insights": math_insights,
                        "ieee_citation": self._format_ieee_citation(title, authors, published, arxiv_id),
                        "bibtex": self._format_bibtex(arxiv_id, title, authors, published),
                    })

                return results
        except Exception as e:
            logger.error("Failed to query arXiv API: %s", str(e))
            return []

    async def get_paper_details(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch structured metadata and details for a specific arXiv paper ID.
        """
        clean_id = arxiv_id.split("/")[-1].replace(".pdf", "")
        url = f"{self.arxiv_api_url}?id_list={clean_id}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    root = ET.fromstring(response.text)
                    namespace = {"atom": "http://www.w3.org/2005/Atom"}
                    entry = root.find("atom:entry", namespace)
                    if entry is not None:
                        title_elem = entry.find("atom:title", namespace)
                        title = " ".join(title_elem.text.split()) if title_elem is not None else ""
                        summary_elem = entry.find("atom:summary", namespace)
                        summary = " ".join(summary_elem.text.split()) if summary_elem is not None else ""
                        published_elem = entry.find("atom:published", namespace)
                        published = published_elem.text.strip() if published_elem is not None else ""

                        authors = [a.find("atom:name", namespace).text.strip() for a in entry.findall("atom:author", namespace) if a.find("atom:name", namespace) is not None]

                        return {
                            "arxiv_id": clean_id,
                            "title": title,
                            "authors": authors,
                            "summary": summary,
                            "published": published,
                            "alphaxiv_url": f"https://alphaxiv.org/abs/{clean_id}",
                            "pdf_url": f"https://arxiv.org/pdf/{clean_id}.pdf",
                            "math_insights": self._extract_math_concepts(summary),
                            "ieee_citation": self._format_ieee_citation(title, authors, published, clean_id),
                        }
                return None
        except Exception as e:
            logger.error("Failed to fetch paper details for %s: %s", arxiv_id, str(e))
            return None

    def _extract_math_concepts(self, text: str) -> Dict[str, Any]:
        """Heuristic extractor for mathematical formulations, loss functions, and ML architectures."""
        equations = re.findall(r"\$[^$]+\$", text)
        equations.extend(re.findall(r"\$\$[^$]+\$\$", text))

        keywords_pde = [kw for kw in ["Navier-Stokes", "diffusion", "heat equation", "advection", "convection", "boundary condition", "Fourier law", "Stefan-Boltzmann"] if kw.lower() in text.lower()]
        keywords_ml = [kw for kw in ["transformer", "PINN", "physics-informed", "GNN", "graph neural network", "diffusion model", "super-resolution", "LSTM", "reinforcement learning", "Pareto"] if kw.lower() in text.lower()]
        keywords_domain = [kw for kw in ["urban heat island", "land surface temperature", "albedo", "evapotranspiration", "thermal comfort", "WBGT", "UTCI", "canopy", "microclimate"] if kw.lower() in text.lower()]

        return {
            "latex_expressions": equations[:5],
            "pde_physics_keywords": keywords_pde,
            "ml_architecture_keywords": keywords_ml,
            "urban_domain_keywords": keywords_domain,
        }

    def _format_ieee_citation(self, title: str, authors: List[str], published: str, arxiv_id: str) -> str:
        year = published[:4] if published else "2024"
        if len(authors) == 1:
            author_str = authors[0]
        elif len(authors) == 2:
            author_str = f"{authors[0]} and {authors[1]}"
        elif len(authors) > 2:
            author_str = f"{authors[0]} et al."
        else:
            author_str = "Anonymous"
        return f"{author_str}, \"{title},\" arXiv preprint arXiv:{arxiv_id}, {year}."

    def _format_bibtex(self, arxiv_id: str, title: str, authors: List[str], published: str) -> str:
        year = published[:4] if published else "2024"
        first_author = authors[0].split()[-1].lower() if authors else "arxiv"
        bib_key = f"{first_author}{year}{arxiv_id.replace('.', '_')[:8]}"
        author_joined = " and ".join(authors)
        return (
            f"@article{{{bib_key},\n"
            f"  author    = {{{author_joined}}},\n"
            f"  title     = {{{{{title}}}}},\n"
            f"  journal   = {{arXiv preprint arXiv:{arxiv_id}}},\n"
            f"  year      = {{{year}}}\n"
            f"}}"
        )
