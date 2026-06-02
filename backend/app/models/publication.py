"""Publication ORM model."""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, ForeignKey, Enum, JSON, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Platform(str, PyEnum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"


class PublicationStatus(str, PyEnum):
    QUEUED = "queued"
    UPLOADING = "uploading"
    PUBLISHED = "published"
    FAILED = "failed"
    SCHEDULED = "scheduled"


class Publication(Base):
    """Tracks content publication to social platforms."""

    __tablename__ = "publications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )

    platform: Mapped[Platform] = mapped_column(Enum(Platform), nullable=False)
    status: Mapped[PublicationStatus] = mapped_column(
        Enum(PublicationStatus), default=PublicationStatus.QUEUED
    )

    # Platform-specific IDs
    platform_video_id: Mapped[str | None] = mapped_column(String(500))
    platform_url: Mapped[str | None] = mapped_column(String(2000))

    # Published content details
    title: Mapped[str | None] = mapped_column(String(1000))
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list | None] = mapped_column(JSON)
    thumbnail_path: Mapped[str | None] = mapped_column(String(2000))

    # Virality score at time of publishing
    virality_score_at_publish: Mapped[float | None] = mapped_column(Float)
    carag_iterations: Mapped[int | None] = mapped_column(Integer)

    # Post-publish analytics (populated via webhook/polling)
    views_count: Mapped[int | None] = mapped_column(Integer)
    likes_count: Mapped[int | None] = mapped_column(Integer)
    comments_count: Mapped[int | None] = mapped_column(Integer)
    shares_count: Mapped[int | None] = mapped_column(Integer)
    watch_time_hours: Mapped[float | None] = mapped_column(Float)
    ctr_percent: Mapped[float | None] = mapped_column(Float)

    # Raw platform response
    platform_response: Mapped[dict | None] = mapped_column(JSON)
    error_message: Mapped[str | None] = mapped_column(Text)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))
    published_by: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<Publication id={self.id} platform={self.platform} "
            f"status={self.status}>"
        )
