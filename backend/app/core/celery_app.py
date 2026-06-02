"""
Celery application configuration with task routing.
"""
from celery import Celery
from celery.schedules import crontab

from backend.app.core.config import settings


def create_celery_app() -> Celery:
    celery = Celery(
        "omniviral",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "backend.app.tasks.ingestion_tasks",
            "backend.app.tasks.prediction_tasks",
            "backend.app.tasks.forecasting_tasks",
            "backend.app.tasks.agent_tasks",
            "backend.app.tasks.publishing_tasks",
            "backend.app.tasks.retraining_tasks",
        ],
    )

    celery.conf.update(
        # Serialization
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,

        # Task behavior
        task_track_started=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        task_soft_time_limit=600,    # 10 min soft limit
        task_time_limit=900,         # 15 min hard limit

        # Retry
        task_max_retries=3,
        task_default_retry_delay=60,

        # Result expiry
        result_expires=86400,  # 24 hours

        # Routing
        task_routes={
            "backend.app.tasks.ingestion_tasks.*": {"queue": "ingestion"},
            "backend.app.tasks.prediction_tasks.*": {"queue": "ml"},
            "backend.app.tasks.forecasting_tasks.*": {"queue": "ml"},
            "backend.app.tasks.agent_tasks.*": {"queue": "agents"},
            "backend.app.tasks.publishing_tasks.*": {"queue": "publishing"},
            "backend.app.tasks.retraining_tasks.*": {"queue": "retraining"},
        },

        # Scheduled tasks (Beat)
        beat_schedule={
            "drift-detection-daily": {
                "task": "backend.app.tasks.retraining_tasks.check_drift",
                "schedule": crontab(hour=2, minute=0),  # 2 AM daily
            },
            "model-retraining-weekly": {
                "task": "backend.app.tasks.retraining_tasks.retrain_models",
                "schedule": crontab(hour=3, minute=0, day_of_week=1),  # Monday 3 AM
            },
            "purge-old-logs": {
                "task": "backend.app.tasks.ingestion_tasks.purge_old_logs",
                "schedule": crontab(hour=1, minute=0),  # 1 AM daily
            },
        },
    )

    return celery


celery_app = create_celery_app()
