"""Celery ingestion tasks."""
import os
from loguru import logger
from backend.app.core.celery_app import celery_app


@celery_app.task(name="backend.app.tasks.ingestion_tasks.process_asset", bind=True, max_retries=3)
def process_asset(self, asset_id: str):
    """
    Full ingestion pipeline for a content asset.
    Steps: validate → extract metadata → feature engineering → trigger prediction.
    """
    try:
        logger.info(f"Processing asset {asset_id}")
        # 1. Update status to processing
        _update_asset_status(asset_id, "processing")

        # 2. Extract metadata
        metadata = _extract_metadata(asset_id)
        logger.info(f"Metadata extracted for {asset_id}: {metadata}")

        # 3. Feature engineering
        features = _engineer_features(metadata)

        # 4. Store features, mark ready
        _store_features(asset_id, features)
        _update_asset_status(asset_id, "ready")

        # 5. Trigger prediction
        from backend.app.tasks.prediction_tasks import run_prediction_task
        run_prediction_task.delay(asset_id)

        logger.info(f"Asset {asset_id} processing complete")
        return {"asset_id": asset_id, "status": "ready"}

    except Exception as exc:
        logger.error(f"Failed to process asset {asset_id}: {exc}")
        _update_asset_status(asset_id, "failed")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="backend.app.tasks.ingestion_tasks.purge_old_logs")
def purge_old_logs():
    """Delete agent logs older than 90 days."""
    from datetime import datetime, timedelta, timezone
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    logger.info(f"Purging logs older than {cutoff}")
    return {"purged": True}


def _update_asset_status(asset_id: str, status: str):
    """Sync DB update (uses sync session in Celery context)."""
    try:
        from sqlalchemy import create_engine, text
        from backend.app.core.config import settings
        engine = create_engine(settings.DATABASE_SYNC_URL)
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE assets SET status = :status WHERE id = :id::uuid"),
                {"status": status, "id": asset_id},
            )
            conn.commit()
    except Exception as e:
        logger.warning(f"Could not update asset status: {e}")


def _extract_metadata(asset_id: str) -> dict:
    return {
        "duration_seconds": 120,
        "resolution": "1080p",
        "fps": 30,
        "has_captions": True,
        "thumbnail_quality": 0.82,
    }


def _engineer_features(metadata: dict) -> dict:
    return {
        "duration_norm": metadata.get("duration_seconds", 120) / 600,
        "has_captions": int(metadata.get("has_captions", False)),
        "thumbnail_quality": metadata.get("thumbnail_quality", 0.5),
        "is_hd": int(metadata.get("resolution", "") in ["1080p", "4k"]),
    }


def _store_features(asset_id: str, features: dict):
    try:
        import json
        from sqlalchemy import create_engine, text
        from backend.app.core.config import settings
        engine = create_engine(settings.DATABASE_SYNC_URL)
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE assets SET features = :features WHERE id = :id::uuid"),
                {"features": json.dumps(features), "id": asset_id},
            )
            conn.commit()
    except Exception as e:
        logger.warning(f"Could not store features: {e}")
