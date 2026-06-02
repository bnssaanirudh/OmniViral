"""Asset ORM model."""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Float, Integer, Text, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class AssetType(str, PyEnum):
    VIDEO = "video"
    SCRIPT = "script"
    IMAGE = "image"
    AUDIO = "audio"
    METADATA = "metadata"


class AssetStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    PUBLISHED = "published"


class Asset(Base):
    """Represents an ingested content asset."""

    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    original_name: Mapped[str] = mapped_column(String(500), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(Enum(AssetType), nullable=False)
    status: Mapped[AssetStatus] = mapped_column(
        Enum(AssetStatus), default=AssetStatus.PENDING, nullable=False
    )

    # Content metadata
    title: Mapped[str | None] = mapped_column(String(1000))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(255))
    language: Mapped[str | None] = mapped_column(String(50))
    region: Mapped[str | None] = mapped_column(String(100))
    platform: Mapped[str | None] = mapped_column(String(100))
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer)

    # Storage
    storage_path: Mapped[str | None] = mapped_column(String(2000))
    s3_key: Mapped[str | None] = mapped_column(String(2000))

    # Feature vector (cached after engineering)
    features: Mapped[dict | None] = mapped_column(JSON)

    # Raw metadata from ingestion
    raw_metadata: Mapped[dict | None] = mapped_column(JSON)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))
    uploaded_by: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"<Asset id={self.id} name={self.original_name} status={self.status}>"
