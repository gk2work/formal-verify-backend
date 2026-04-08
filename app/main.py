"""
Formal Verify — FastAPI Application Entry Point

Run with: uvicorn app.main:app --reload --port 8000
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, formal, sva
from app.services.formal_service import formal_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger("formalverify")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Formal Verify starting...")

    info = formal_service.health()
    if info["sby"] == "available":
        logger.info(f"sby: {info['sby_path']}")
    else:
        logger.warning("SymbiYosys (sby) not found. Install OSS CAD Suite.")

    if info["yosys"] == "available":
        logger.info(f"yosys: {info['yosys_path']}")
    else:
        logger.warning("yosys not found.")

    logger.info("Formal Verify ready.")
    yield
    logger.info("Formal Verify shutdown complete.")


app = FastAPI(
    title="Formal Verify",
    description="Formal Verification Tool — SVA + SymbiYosys",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sva.router)
app.include_router(formal.router)


@app.get("/")
async def root():
    return {
        "name": "Formal Verify",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "formal_run_upload": "/api/formal/run-upload",
            "formal_status": "/api/formal/status/{job_id}",
            "formal_counterexample": "/api/formal/counterexample/{job_id}",
            "docs": "/docs",
        },
    }
