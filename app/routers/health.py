"""
Formal Verify — Health Router

GET /api/health  — System health check (sby + yosys)
"""

import logging
from fastapi import APIRouter
from app.services.formal_service import formal_service

logger = logging.getLogger("formalverify.health")
router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health():
    """System health: sby and yosys availability."""
    info = formal_service.health()
    return {
        "sby": info["sby"],
        "yosys": info["yosys"],
        "status": "ok" if info["sby"] == "available" else "degraded",
        "active_jobs": info["active_jobs"],
        "total_jobs": info["total_jobs"],
    }
