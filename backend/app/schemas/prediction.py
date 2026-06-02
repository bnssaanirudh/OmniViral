"""Pydantic schemas for Prediction."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.app.models.prediction import RiskLevel


class PredictionRequest(BaseModel):
    asset_id: uuid.UUID
    use_ensemble: bool = True
    explain: bool = True


class PredictionResponse(BaseModel):
    id: uuid.UUID
    asset_id: uuid.UUID
    risk_level: RiskLevel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    virality_score: float = Field(..., ge=0.0, le=1.0)
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    lr_score: Optional[float] = None
    dt_score: Optional[float] = None
    nb_score: Optional[float] = None
    knn_score: Optional[float] = None
    svm_score: Optional[float] = None
    rf_score: Optional[float] = None
    xgb_score: Optional[float] = None
    ensemble_score: Optional[float] = None
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    roc_auc: Optional[float] = None
    shap_values: Optional[dict] = None
    feature_importance: Optional[dict] = None
    explanation_text: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    rank: int
    model_name: str
    accuracy: float
    f1_score: float
    roc_auc: float
    is_champion: bool
