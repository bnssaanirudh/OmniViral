"""ModelMetric ORM model — tracks ML experiment and evaluation results."""
import uuid

from sqlalchemy import String, Float, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class ModelMetric(Base):
    """Stores model training/evaluation metrics from MLflow or direct runs."""

    __tablename__ = "model_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # MLflow integration
    mlflow_run_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    mlflow_experiment_id: Mapped[str | None] = mapped_column(String(255))

    # Model identity
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    model_type: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "xgboost"
    model_version: Mapped[str | None] = mapped_column(String(100))
    is_champion: Mapped[bool] = mapped_column(default=False)

    # Classification metrics
    accuracy: Mapped[float | None] = mapped_column(Float)
    precision: Mapped[float | None] = mapped_column(Float)
    recall: Mapped[float | None] = mapped_column(Float)
    f1_score: Mapped[float | None] = mapped_column(Float)
    roc_auc: Mapped[float | None] = mapped_column(Float)

    # Regression / forecast metrics
    mae: Mapped[float | None] = mapped_column(Float)
    mse: Mapped[float | None] = mapped_column(Float)
    rmse: Mapped[float | None] = mapped_column(Float)
    mape: Mapped[float | None] = mapped_column(Float)

    # Training info
    training_samples: Mapped[int | None] = mapped_column(Integer)
    validation_samples: Mapped[int | None] = mapped_column(Integer)
    training_duration_seconds: Mapped[float | None] = mapped_column(Float)
    hyperparameters: Mapped[dict | None] = mapped_column(JSON)

    # Feature importance
    feature_importance: Mapped[dict | None] = mapped_column(JSON)

    # Drift detection
    drift_score: Mapped[float | None] = mapped_column(Float)
    drift_detected: Mapped[bool | None] = mapped_column(default=False)

    # Leaderboard position
    leaderboard_rank: Mapped[int | None] = mapped_column(Integer)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<ModelMetric id={self.id} model={self.model_name} "
            f"f1={self.f1_score} champion={self.is_champion}>"
        )
