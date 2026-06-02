"""
OmniViral FastAPI Application Entry Point
"""
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator

from backend.app.api.routes import (
    auth,
    dashboard,
    forecast,
    ingest,
    metrics,
    optimize,
    predict,
    publish,
)
from backend.app.core.config import settings
from backend.app.core.database import engine, Base
from backend.app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events."""
    setup_logging()
    # Create all tables on startup (dev mode; use Alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def create_application() -> FastAPI:
    app = FastAPI(
        title="OmniViral API",
        description=(
            "Autonomous Multi-Modal Predictive Content Lifecycle Forecaster "
            "& Agentic Creative Optimization Engine"
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── Middleware ────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],  # Restrict in production
    )

    # ── Prometheus Instrumentation ────────────────────────────────────────────
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_group_untemplated=True,
        excluded_handlers=["/metrics", "/health"],
    ).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)

    # ── Routers ───────────────────────────────────────────────────────────────
    prefix = "/api/v1"
    app.include_router(auth.router, prefix=f"{prefix}/auth", tags=["Authentication"])
    app.include_router(ingest.router, prefix=f"{prefix}/ingest", tags=["Ingestion"])
    app.include_router(predict.router, prefix=f"{prefix}/predict", tags=["Prediction"])
    app.include_router(forecast.router, prefix=f"{prefix}/forecast", tags=["Forecasting"])
    app.include_router(optimize.router, prefix=f"{prefix}/optimize", tags=["Optimization"])
    app.include_router(publish.router, prefix=f"{prefix}/publish", tags=["Publishing"])
    app.include_router(metrics.router, prefix=f"{prefix}/metrics", tags=["Metrics"])
    app.include_router(dashboard.router, prefix=f"{prefix}/dashboard", tags=["Dashboard"])

    # ── Health Check ──────────────────────────────────────────────────────────
    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "healthy",
            "version": "1.0.0",
            "service": "OmniViral API",
        }

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "message": "Welcome to OmniViral API",
            "docs": "/docs",
            "health": "/health",
        }

    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
