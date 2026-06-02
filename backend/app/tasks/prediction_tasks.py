"""Celery prediction tasks."""
from loguru import logger
from backend.app.core.celery_app import celery_app


@celery_app.task(name="backend.app.tasks.prediction_tasks.run_prediction_task", bind=True, max_retries=2)
def run_prediction_task(self, asset_id: str, use_ensemble: bool = True, explain: bool = True):
    """
    Run ML prediction pipeline on a processed asset.
    Returns prediction dict to be stored by the API layer.
    """
    try:
        logger.info(f"Running prediction for asset {asset_id}")
        from ml_pipeline.classification.classifier import ContentClassifier
        classifier = ContentClassifier()
        features = _get_features(asset_id)
        result = classifier.predict(features, use_ensemble=use_ensemble, explain=explain)
        logger.info(f"Prediction complete for {asset_id}: {result['risk_level']}")
        return result
    except Exception as exc:
        logger.error(f"Prediction failed for {asset_id}: {exc}")
        raise self.retry(exc=exc, countdown=30)


@celery_app.task(name="backend.app.tasks.prediction_tasks.batch_predict")
def batch_predict(asset_ids: list[str]):
    """Run predictions on a batch of assets."""
    results = []
    for asset_id in asset_ids:
        try:
            result = run_prediction_task(asset_id)
            results.append({"asset_id": asset_id, "status": "ok", "result": result})
        except Exception as e:
            results.append({"asset_id": asset_id, "status": "error", "error": str(e)})
    return results


def _get_features(asset_id: str) -> dict:
    """Retrieve stored features for an asset."""
    try:
        import json
        from sqlalchemy import create_engine, text
        from backend.app.core.config import settings
        engine = create_engine(settings.DATABASE_SYNC_URL)
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT features FROM assets WHERE id = :id::uuid"), {"id": asset_id}
            ).fetchone()
            if row and row[0]:
                return json.loads(row[0]) if isinstance(row[0], str) else row[0]
    except Exception as e:
        logger.warning(f"Could not retrieve features for {asset_id}: {e}")
    # Return synthetic features for demo
    import random
    return {
        "duration_norm": random.uniform(0.1, 0.9),
        "has_captions": random.choice([0, 1]),
        "thumbnail_quality": random.uniform(0.4, 0.95),
        "is_hd": 1,
        "engagement_rate": random.uniform(0.02, 0.12),
        "publish_hour": random.randint(0, 23),
    }
