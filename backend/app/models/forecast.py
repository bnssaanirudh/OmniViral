"""Forecast ORM model."""
import uuid

from sqlalchemy import String, Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Forecast(Base):
    """90-day content lifecycle forecast."""

    __tablename__ = "forecasts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )

    # Forecast horizon
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, default=90)
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(100))

    # Time series output (JSON arrays: [{day, value}])
    daily_views_forecast: Mapped[dict | None] = mapped_column(JSON)
    daily_watch_time_forecast: Mapped[dict | None] = mapped_column(JSON)
    daily_ctr_forecast: Mapped[dict | None] = mapped_column(JSON)
    daily_engagement_forecast: Mapped[dict | None] = mapped_column(JSON)

    # Summary metrics
    peak_views_day: Mapped[int | None] = mapped_column(Integer)
    peak_views_value: Mapped[float | None] = mapped_column(Float)
    saturation_day: Mapped[int | None] = mapped_column(Integer)
    plateau_day: Mapped[int | None] = mapped_column(Integer)
    total_projected_views: Mapped[float | None] = mapped_column(Float)
    velocity_score: Mapped[float | None] = mapped_column(Float)
    growth_rate_percent: Mapped[float | None] = mapped_column(Float)

    # Confidence intervals
    lower_bound: Mapped[dict | None] = mapped_column(JSON)
    upper_bound: Mapped[dict | None] = mapped_column(JSON)

    # Plot artifacts
    forecast_plot_path: Mapped[str | None] = mapped_column(String(2000))

    # Explanation
    narrative: Mapped[str | None] = mapped_column(Text)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<Forecast id={self.id} asset={self.asset_id} "
            f"model={self.model_name} horizon={self.forecast_horizon_days}d>"
        )
