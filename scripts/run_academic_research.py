"""
Academic Literature Research & Synthesis Pipeline
Leverages AlphaXivClient (arXiv + alphaXiv) to systematically research foundational papers
for Thermal Sentinel Grid and FortyGuard Hackathon.
"""

import asyncio
import json
import os
import sys
from typing import Dict, List, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.api.alphaxiv_client import AlphaXivClient

RESEARCH_DOMAINS = {
    "physics_informed_thermal_pdes": {
        "title": "Physics-Informed Neural Networks (PINNs) & Thermal PDEs",
        "description": "Solving 2D/3D thermal advection-diffusion, Navier-Stokes buoyancy, and Fourier conduction in urban geometry.",
        "queries": [
            "physics informed neural network thermal conduction diffusion",
            "PINN urban microclimate heat transfer",
            "physics informed machine learning temperature forecasting advection",
        ],
        "limit_per_query": 4,
    },
    "thermal_remote_sensing_superres": {
        "title": "High-Resolution Satellite Thermal Downscaling & Super-Resolution",
        "description": "Downscaling Landsat, MODIS, and ECOSTRESS Land Surface Temperature (LST) to metric scales.",
        "queries": [
            "land surface temperature super resolution deep learning",
            "thermal infrared downscaling remote sensing MODIS Landsat",
            "satellite thermal imagery spatial resolution enhancement neural network",
        ],
        "limit_per_query": 4,
    },
    "urban_heat_island_forecasting": {
        "title": "Urban Heat Island (UHI) & Microclimate Dynamics Forecasting",
        "description": "Graph Neural Networks, Spatio-Temporal Transformers, and Urban Canopy Models for heat forecasting.",
        "queries": [
            "urban heat island forecasting spatio-temporal graph neural network",
            "urban canopy microclimate temperature prediction deep learning",
            "urban thermal environment heat wave extreme temperature modeling",
        ],
        "limit_per_query": 4,
    },
    "mitigation_albedo_greenery": {
        "title": "Urban Heat Mitigation: Cool Pavements, Albedo & Evapotranspiration",
        "description": "Countermeasure effectiveness: high-albedo coatings, permeable pavement, tree canopy shade, and urban vegetation.",
        "queries": [
            "cool pavement urban heat island mitigation albedo",
            "urban greenery evapotranspiration temperature reduction modeling",
            "urban heat mitigation strategies optimization Pareto multi-objective",
        ],
        "limit_per_query": 4,
    },
    "multi_agent_resilience_decision": {
        "title": "Autonomous Multi-Agent & Reinforcement Learning for Urban Climate Resilience",
        "description": "Agentic coordination, Pareto frontier optimization, and infrastructure adaptation planning.",
        "queries": [
            "multi-agent reinforcement learning urban climate adaptation",
            "climate resilience urban planning optimization Pareto",
            "autonomous LLM multi-agent scientific workflow decision support",
        ],
        "limit_per_query": 4,
    }
}

async def run_domain_research() -> Dict[str, Any]:
    client = AlphaXivClient()
    corpus = {}
    total_papers_found = 0
    seen_ids = set()

    print("=" * 80)
    print("STARTING SCIENTIFIC LITERATURE DISCOVERY VIA ALPHAXIV / ARXIV CLIENT")
    print("=" * 80)

    for domain_key, domain_info in RESEARCH_DOMAINS.items():
        print(f"\n🔬 Exploring Domain: {domain_info['title']}...")
        corpus[domain_key] = {
            "title": domain_info["title"],
            "description": domain_info["description"],
            "papers": [],
        }

        for query in domain_info["queries"]:
            print(f"  🔍 Query: '{query}'")
            papers = await client.search_papers(query, limit=domain_info["limit_per_query"])
            for p in papers:
                if p["arxiv_id"] not in seen_ids:
                    seen_ids.add(p["arxiv_id"])
                    corpus[domain_key]["papers"].append(p)
                    total_papers_found += 1
                    print(f"    📄 [{p['arxiv_id']}] {p['title'][:70]}... ({p['published'][:10]})")
            # Sleep slightly to respect polite rate limiting
            await asyncio.sleep(1.5)

    print("\n" + "=" * 80)
    print(f"✅ RESEARCH DISCOVERY COMPLETE: {total_papers_found} unique papers retrieved across {len(RESEARCH_DOMAINS)} domains.")
    print("=" * 80)

    # Save raw research corpus JSON
    os.makedirs("docs/research", exist_ok=True)
    corpus_path = "docs/research/alphaxiv_research_corpus.json"
    with open(corpus_path, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)
    print(f"Saved raw research corpus to: {corpus_path}")

    return corpus

if __name__ == "__main__":
    asyncio.run(run_domain_research())
