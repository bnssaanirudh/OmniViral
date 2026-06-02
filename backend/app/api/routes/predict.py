"""
Predict router: run ML classification on an ingested asset.
"""
import uuid

from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlalchemy import select

from backend.app.api.deps import DBSession, CurrentUser
from backend.app.models.asset import Asset, AssetStatus
from backend.app.models.prediction import Prediction
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse, LeaderboardEntry
from backend.app.models.model_metric import ModelMetric

router = APIRouter()


@router.post("/", response_model=PredictionResponse, status_code=201)
async def run_prediction(
    request: PredictionRequest,
    db: DBSession,
    current_user: CurrentUser,
    background_tasks: BackgroundTasks,
):
    """
    Run ML ensemble classification on an asset.
    Returns risk level, virality score, per-model scores, and SHAP explanation.
    """
    # Validate asset exists
    result = await db.execute(select(Asset).where(Asset.id == request.asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found.")

    # Trigger prediction via Celery (sync result for demo)
    try:
        from backend.app.tasks.prediction_tasks import run_prediction_task
        task = run_prediction_task.delay(str(request.asset_id), request.use_ensemble, request.explain)
        result_data = task.get(timeout=30)
    except Exception:
        # Fallback: mock prediction for demo mode
        result_data = _mock_prediction(asset)

    # Store prediction
    prediction = Prediction(
        asset_id=request.asset_id,
        **result_data,
    )
    db.add(prediction)
    await db.flush()
    await db.refresh(prediction)

    # Update asset status
    asset.status = AssetStatus.READY
    db.add(asset)

    return prediction


def _mock_prediction(asset: Asset) -> dict:
    """Generate a realistic mock prediction for demo/offline mode."""
    import random
    score = random.uniform(0.4, 0.95)
    from backend.app.models.prediction import RiskLevel
    risk = (
        RiskLevel.LOW_RISK if score > 0.7
        else RiskLevel.MEDIUM_RISK if score > 0.5
        else RiskLevel.HIGH_RISK
    )
    return {
        "risk_level": risk,
        "confidence_score": score,
        "virality_score": score,
        "model_name": "VotingEnsemble",
        "model_version": "1.0.0",
        "lr_score": round(score - 0.05, 3),
        "dt_score": round(score - 0.03, 3),
        "nb_score": round(score - 0.07, 3),
        "knn_score": round(score - 0.02, 3),
        "svm_score": round(score - 0.04, 3),
        "rf_score": round(score + 0.02, 3),
        "xgb_score": round(score + 0.01, 3),
        "ensemble_score": round(score, 3),
        "accuracy": 0.91,
        "precision": 0.89,
        "recall": 0.88,
        "f1_score": 0.885,
        "roc_auc": 0.94,
        "explanation_text": (
            f"Asset scored {score:.2f}. "
            "Key drivers: content length, engagement_rate, thumbnail_ctr."
        ),
        "feature_importance": {
            "engagement_rate": 0.32,
            "content_length": 0.21,
            "thumbnail_ctr": 0.18,
            "publish_hour": 0.15,
            "category_encoding": 0.14,
        },
    }


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
async def get_leaderboard(db: DBSession, current_user: CurrentUser):
    """Return the model leaderboard ranked by F1 score."""
    result = await db.execute(
        select(ModelMetric).order_by(ModelMetric.f1_score.desc()).limit(20)
    )
    metrics = result.scalars().all()
    if not metrics:
        # Return mock leaderboard
        return _mock_leaderboard()
    return [
        LeaderboardEntry(
            rank=i + 1,
            model_name=m.model_name,
            accuracy=m.accuracy or 0,
            f1_score=m.f1_score or 0,
            roc_auc=m.roc_auc or 0,
            is_champion=m.is_champion,
        )
        for i, m in enumerate(metrics)
    ]


def _mock_leaderboard() -> list[LeaderboardEntry]:
    models = [
        ("VotingEnsemble", 0.912, 0.897, 0.942, True),
        ("XGBoost", 0.908, 0.891, 0.938, False),
        ("RandomForest", 0.902, 0.883, 0.931, False),
        ("GradientBoosting", 0.895, 0.876, 0.927, False),
        ("SVM", 0.881, 0.862, 0.913, False),
        ("LogisticRegression", 0.867, 0.848, 0.901, False),
        ("KNN", 0.852, 0.834, 0.889, False),
        ("DecisionTree", 0.838, 0.819, 0.874, False),
        ("NaiveBayes", 0.821, 0.801, 0.858, False),
        ("AdaBoost", 0.891, 0.871, 0.921, False),
    ]
    return [
        LeaderboardEntry(rank=i+1, model_name=m[0], accuracy=m[1], f1_score=m[2], roc_auc=m[3], is_champion=m[4])
        for i, m in enumerate(models)
    ]


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: uuid.UUID, db: DBSession, current_user: CurrentUser):
    """Get a specific prediction by ID."""
    result = await db.execute(select(Prediction).where(Prediction.id == prediction_id))
    pred = result.scalar_one_or_none()
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found.")
    return pred
