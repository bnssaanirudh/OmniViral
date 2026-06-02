"""Celery agent and retraining tasks."""
from loguru import logger
from backend.app.core.celery_app import celery_app


@celery_app.task(name="backend.app.tasks.agent_tasks.run_carag_loop", bind=True, max_retries=1)
def run_carag_loop(self, asset_id: str, max_iterations: int = 3, target_score: float = 0.75):
    """Run the CARAG multi-agent optimization loop."""
    try:
        from agents.carag.orchestrator import CaragOrchestrator
        orchestrator = CaragOrchestrator()
        result = orchestrator.run(asset_id, max_iterations, target_score)
        return result
    except Exception as exc:
        logger.error(f"CARAG loop failed for {asset_id}: {exc}")
        raise self.retry(exc=exc, countdown=10)


@celery_app.task(name="backend.app.tasks.retraining_tasks.check_drift")
def check_drift():
    """Detect model drift and trigger retraining if needed."""
    try:
        from ml_pipeline.drift.drift_detector import DriftDetector
        detector = DriftDetector()
        result = detector.check()
        if result["drift_detected"]:
            logger.warning(f"Drift detected! PSI={result['psi_score']:.4f}. Triggering retrain.")
            retrain_models.delay()
        return result
    except Exception as e:
        logger.error(f"Drift check failed: {e}")
        return {"drift_detected": False, "error": str(e)}


@celery_app.task(name="backend.app.tasks.retraining_tasks.retrain_models")
def retrain_models():
    """Retrain all ML models with fresh data."""
    try:
        from ml_pipeline.ensemble_engine import EnsembleEngine
        engine = EnsembleEngine()
        result = engine.retrain()
        logger.info(f"Retraining complete: {result}")
        return result
    except Exception as e:
        logger.error(f"Retraining failed: {e}")
        return {"status": "failed", "error": str(e)}


@celery_app.task(name="backend.app.tasks.publishing_tasks.publish_to_platform")
def publish_to_platform(asset_id: str, platform: str, metadata: dict):
    """Celery task wrapping the publishing adapter."""
    try:
        from agents.publishing.publisher import get_publisher
        from backend.app.models.publication import Platform as PlatformEnum
        publisher = get_publisher(PlatformEnum(platform))
        import asyncio
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(
            publisher.publish_by_id(asset_id=asset_id, **metadata)
        )
        loop.close()
        return result
    except Exception as e:
        logger.error(f"Publishing failed: {e}")
        raise
