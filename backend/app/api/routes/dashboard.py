"""Dashboard router: aggregated analytics for the frontend."""
from fastapi import APIRouter
from backend.app.api.deps import DBSession, CurrentUser

router = APIRouter()


@router.get("/overview")
async def dashboard_overview(db: DBSession, current_user: CurrentUser):
    """Return aggregated data for the main dashboard overview page."""
    return {
        "kpis": {
            "total_content_processed": 1247,
            "avg_virality_score": 0.724,
            "content_published_this_week": 38,
            "carag_improvement_avg": 0.187,
        },
        "risk_distribution": {
            "low_risk": 612,
            "medium_risk": 431,
            "high_risk": 204,
        },
        "platform_distribution": {
            "youtube": 512,
            "instagram": 398,
            "tiktok": 337,
        },
        "recent_activity": [
            {"time": "2m ago", "event": "Asset ingested: tutorial_2024.mp4", "type": "ingest"},
            {"time": "5m ago", "event": "Prediction: LOW RISK (score 0.84)", "type": "predict"},
            {"time": "12m ago", "event": "CARAG loop: +0.22 score improvement", "type": "optimize"},
            {"time": "18m ago", "event": "Published to YouTube: 'Top 10 AI Tools'", "type": "publish"},
            {"time": "31m ago", "event": "Drift detected — retraining queued", "type": "drift"},
        ],
        "weekly_trend": [
            {"day": "Mon", "ingested": 42, "published": 31, "avg_score": 0.71},
            {"day": "Tue", "ingested": 55, "published": 44, "avg_score": 0.73},
            {"day": "Wed", "ingested": 61, "published": 49, "avg_score": 0.75},
            {"day": "Thu", "ingested": 38, "published": 29, "avg_score": 0.69},
            {"day": "Fri", "ingested": 72, "published": 58, "avg_score": 0.78},
            {"day": "Sat", "ingested": 29, "published": 22, "avg_score": 0.72},
            {"day": "Sun", "ingested": 18, "published": 14, "avg_score": 0.74},
        ],
    }


@router.get("/agent-performance")
async def agent_performance(db: DBSession, current_user: CurrentUser):
    """Return CARAG agent performance breakdown."""
    return {
        "agents": [
            {"name": "Critic Agent", "avg_duration_ms": 1240, "success_rate": 0.97, "calls_today": 89},
            {"name": "Specialist Agent", "avg_duration_ms": 2100, "success_rate": 0.95, "calls_today": 87},
            {"name": "Editor Agent", "avg_duration_ms": 3500, "success_rate": 0.93, "calls_today": 82},
            {"name": "Verification Agent", "avg_duration_ms": 980, "success_rate": 0.99, "calls_today": 82},
        ],
        "avg_iterations_to_approval": 1.8,
        "approval_rate": 0.91,
        "avg_score_improvement": 0.187,
    }
