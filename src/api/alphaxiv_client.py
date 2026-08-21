"""
alphaXiv API Client - Scientific Paper Fetcher & Academic Provenance Adapter
Allows Thermal Sentinel Grid agents to dynamically search arXiv papers, retrieve
mathematical models, and generate verified academic citations.
"""

import os
import logging
from typing import Dict, Any, List, Optional
import httpx

logger = logging.getLogger("thermal_sentinel.alphaxiv")

class AlphaXivClient:
    """
    Client for interacting with the alphaXiv API (https://api.alphaxiv.org).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.alphaxiv.org/v1",
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.getenv("ALPHAXIV_API_KEY", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ThermalSentinelGrid/1.0",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def search_papers(
        self,
        query: str,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search arXiv / alphaXiv library for papers matching a query.
        """
        url = f"{self.base_url}/search"
        params = {"q": query, "limit": limit}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers(), params=params)
                if response.status_code == 200:
                    return response.json().get("results", [])
                else:
                    logger.warning(
                        "alphaXiv search returned status %d: %s",
                        response.status_code,
                        response.text,
                    )
                    return []
        except Exception as e:
            logger.error("Failed to query alphaXiv API: %s", str(e))
            return []

    async def get_paper_details(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch structured metadata, mathematical summary, and discussion for a specific arXiv paper.
        """
        url = f"{self.base_url}/papers/{arxiv_id}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=self._get_headers())
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            logger.error("Failed to fetch paper details for %s: %s", arxiv_id, str(e))
            return None
