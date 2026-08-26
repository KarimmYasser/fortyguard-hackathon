"""
Thermal Sentinel Grid - FastAPI Application
Physics-Constrained Agentic Thermal Resilience & Dispatch Backend.
"""

from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv

load_dotenv()

from src.server.routes import (
    scan_router,
    assets_router,
    replay_router,
    dispatch_router,
    sandbox_router,
    benchmark_router,
    power_flow_router,
    research_router,
    advanced_physics_router,
    database_router,
    analytics_router,
    operations_router,
    validation_router,
)

app = FastAPI(
    title="⚡ Thermal Sentinel Grid API",
    description="Physics-Constrained Multi-Agent Thermal Resilience & Dispatch Engine (Tracks 06 & 02)",
    version="1.0.0",
)

# Browser access is limited to the judge-facing production origins and local
# development. CORS is not authentication, but avoiding a wildcard prevents an
# unrelated website from driving this API through a visitor's browser.
ALLOWED_ORIGINS = [
    "https://www.thermal-sentinel-grid.live",
    "https://thermal-sentinel-grid.live",
    "https://thermal-sentinel-grid.vercel.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Apply low-risk browser hardening without changing judge access."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=(), usb=()"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# Mount API routes
app.include_router(scan_router, prefix="/api/v1")
app.include_router(assets_router, prefix="/api/v1")
app.include_router(replay_router, prefix="/api/v1")
app.include_router(dispatch_router, prefix="/api/v1")
app.include_router(sandbox_router, prefix="/api/v1")
app.include_router(benchmark_router)
app.include_router(power_flow_router)
app.include_router(research_router)
app.include_router(advanced_physics_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(operations_router, prefix="/api/v1")
app.include_router(validation_router, prefix="/api/v1")




@app.get("/health", tags=["System Health"])
@app.get("/api/health", tags=["System Health"])
@app.get("/v1/health", tags=["System Health"])
@app.get("/api/v1/health", tags=["System Health"])
@app.get("/api", tags=["System Health"])
@app.get("/api/", tags=["System Health"])
@app.get("/api/index.py", tags=["System Health"])
async def health_check():
    """System health check and FortyGuard API status."""
    mock_mode = os.getenv("MOCK_FORTYGUARD_API", "").lower() in ("true", "1", "yes") or not bool(os.getenv("FORTYGUARD_API_KEY"))
    return {
        "status": "healthy",
        "service": "Thermal Sentinel Grid Backend",
        "version": "1.0.0",
        "mock_mode": mock_mode,
        "active_scenario": "Phoenix July 2023 Heatwave",
        # Provenance is reported per-response on the analytics payloads
        # (data_source: fortyguard_live | fortyguard_live_partial |
        # phoenix_fixture). mock_mode alone only reflects configuration, not
        # whether a given response actually came back from the live API.
        "live_api_configured": not mock_mode,
        "analysis_date": os.getenv("FORTYGUARD_ANALYSIS_DATE", "2023-07-19"),
    }


# Mount rendered videos directory if available
videos_dir = Path(__file__).parents[2] / "videos" / "thermal-sentinel-pitch" / "renders"
if videos_dir.exists():
    app.mount("/videos", StaticFiles(directory=str(videos_dir)), name="videos")

# Mount built frontend if available
frontend_dist = Path(__file__).parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server.main:app", host="0.0.0.0", port=8000, reload=True)
