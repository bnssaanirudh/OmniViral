"""Prediction ORM model."""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, Float, ForeignKey, Enum, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class RiskLevel(str, PyEnum):
    HIGH_RISK = "high_risk"
    MEDIUM_RISK = "medium_risk"
    LOW_RISK = "low_risk"


class Prediction(Base):
    """Stores ML model predictions for a content asset."""

    __tablename__ = "predictions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )

    # Risk classification
    risk_level: Mapped[RiskLevel] = mapped_column(Enum(RiskLevel), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    virality_score: Mapped[float] = mapped_column(Float, nullable=False)

    # Per-model scores
    lr_score: Mapped[float | None] = mapped_column(Float)
    dt_score: Mapped[float | None] = mapped_column(Float)
    nb_score: Mapped[float | None] = mapped_column(Float)
    knn_score: Mapped[float | None] = mapped_column(Float)
    svm_score: Mapped[float | None] = mapped_column(Float)
    rf_score: Mapped[float | None] = mapped_column(Float)
    xgb_score: Mapped[float | None] = mapped_column(Float)
    ensemble_score: Mapped[float | None] = mapped_column(Float)

    # Best model used
    model_name: Mapped[str | None] = mapped_column(String(255))
    model_version: Mapped[str | None] = mapped_column(String(100))

    # Metrics
    accuracy: Mapped[float | None] = mapped_column(Float)
    precision: Mapped[float | None] = mapped_column(Float)
    recall: Mapped[float | None] = mapped_column(Float)
    f1_score: Mapped[float | None] = mapped_column(Float)
    roc_auc: Mapped[float | None] = mapped_column(Float)

    # SHAP explanation
    shap_values: Mapped[dict | None] = mapped_column(JSON)
    feature_importance: Mapped[dict | None] = mapped_column(JSON)
    explanation_text: Mapped[str | None] = mapped_column(Text)

    # Raw prediction output
    raw_output: Mapped[dict | None] = mapped_column(JSON)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<Prediction id={self.id} asset={self.asset_id} "
            f"risk={self.risk_level} score={self.virality_score:.3f}>"
        )
