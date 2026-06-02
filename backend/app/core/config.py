"""
Application configuration using Pydantic Settings.
"""
from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── App ───────────────────────────────────────────────────────────────────
    APP_NAME: str = "OmniViral"
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-to-something-very-long-and-random"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [o.strip() for o in v.split(",")]
        return v

    # ── Database ───────────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://omni:omnipass@localhost:5432/omniviral"
    DATABASE_SYNC_URL: str = "postgresql://omni:omnipass@localhost:5432/omniviral"
    POSTGRES_USER: str = "omni"
    POSTGRES_PASSWORD: str = "omnipass"
    POSTGRES_DB: str = "omniviral"

    # ── Redis ──────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # ── JWT Auth ───────────────────────────────────────────────────────────────
    JWT_SECRET_KEY: str = "jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── MLflow ────────────────────────────────────────────────────────────────
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "omniviral-experiments"

    # ── ChromaDB ──────────────────────────────────────────────────────────────
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION_NAME: str = "content_knowledge_base"

    # ── LLM ───────────────────────────────────────────────────────────────────
    LLM_PROVIDER: str = "mock"
    LLM_MODEL: str = "gpt-4o"
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    # ── Storage ───────────────────────────────────────────────────────────────
    STORAGE_BACKEND: str = "local"
    LOCAL_STORAGE_PATH: str = "./data/uploads"
    INCOMING_VIDEOS_PATH: str = "./incoming/videos"
    INCOMING_SCRIPTS_PATH: str = "./incoming/scripts"
    INCOMING_METADATA_PATH: str = "./incoming/metadata"
    S3_BUCKET_NAME: str = "omniviral-assets"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: Optional[str] = None

    # ── Publishing ────────────────────────────────────────────────────────────
    YOUTUBE_API_KEY: Optional[str] = None
    YOUTUBE_CHANNEL_ID: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    TIKTOK_API_KEY: Optional[str] = None

    # ── Gatekeeper ────────────────────────────────────────────────────────────
    GATEKEEPER_SCORE_THRESHOLD: float = 0.65
    GATEKEEPER_MAX_CARAG_ITERATIONS: int = 3

    # ── Monitoring ────────────────────────────────────────────────────────────
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
