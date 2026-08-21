"""
Unit and Integration Tests for Academic Research & alphaXiv API Router
"""

import pytest
from fastapi.testclient import TestClient
from src.server.main import app

client = TestClient(app)


def test_research_corpus_endpoint():
    response = client.get("/api/v1/research/corpus")
    assert response.status_code == 200
    data = response.json()
    assert "physics_informed_thermal_pdes" in data
    assert "thermal_remote_sensing_superres" in data
    assert "mitigation_albedo_greenery" in data
    assert len(data["mitigation_albedo_greenery"]["papers"]) > 0


def test_research_search_endpoint():
    response = client.get("/api/v1/research/search?query=cool+pavements+albedo&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert "papers" in data
    assert data["count"] > 0
    first_paper = data["papers"][0]
    assert "title" in first_paper
    assert "arxiv_id" in first_paper
    assert "alphaxiv_url" in first_paper
