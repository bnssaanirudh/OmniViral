"""Initial database schema migration."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── assets ────────────────────────────────────────────────────────────────
    op.create_table(
        "assets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("original_name", sa.String(500), nullable=False),
        sa.Column("asset_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("title", sa.String(1000)),
        sa.Column("description", sa.Text()),
        sa.Column("category", sa.String(255)),
        sa.Column("language", sa.String(50)),
        sa.Column("region", sa.String(100)),
        sa.Column("platform", sa.String(100)),
        sa.Column("duration_seconds", sa.Float()),
        sa.Column("file_size_bytes", sa.Integer()),
        sa.Column("storage_path", sa.String(2000)),
        sa.Column("s3_key", sa.String(2000)),
        sa.Column("features", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("raw_metadata", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("uploaded_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_assets_status", "assets", ["status"])
    op.create_index("ix_assets_tenant_id", "assets", ["tenant_id"])
    op.create_index("ix_assets_asset_type", "assets", ["asset_type"])

    # ── predictions ───────────────────────────────────────────────────────────
    op.create_table(
        "predictions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("risk_level", sa.String(50), nullable=False),
        sa.Column("confidence_score", sa.Float(), nullable=False),
        sa.Column("virality_score", sa.Float(), nullable=False),
        sa.Column("lr_score", sa.Float()), sa.Column("dt_score", sa.Float()),
        sa.Column("nb_score", sa.Float()), sa.Column("knn_score", sa.Float()),
        sa.Column("svm_score", sa.Float()), sa.Column("rf_score", sa.Float()),
        sa.Column("xgb_score", sa.Float()), sa.Column("ensemble_score", sa.Float()),
        sa.Column("model_name", sa.String(255)), sa.Column("model_version", sa.String(100)),
        sa.Column("accuracy", sa.Float()), sa.Column("precision", sa.Float()),
        sa.Column("recall", sa.Float()), sa.Column("f1_score", sa.Float()),
        sa.Column("roc_auc", sa.Float()),
        sa.Column("shap_values", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("feature_importance", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("explanation_text", sa.Text()),
        sa.Column("raw_output", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_predictions_asset_id", "predictions", ["asset_id"])
    op.create_index("ix_predictions_risk_level", "predictions", ["risk_level"])

    # ── forecasts ─────────────────────────────────────────────────────────────
    op.create_table(
        "forecasts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("forecast_horizon_days", sa.Integer(), default=90),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("model_version", sa.String(100)),
        sa.Column("daily_views_forecast", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("daily_watch_time_forecast", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("daily_ctr_forecast", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("daily_engagement_forecast", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("peak_views_day", sa.Integer()),
        sa.Column("peak_views_value", sa.Float()),
        sa.Column("saturation_day", sa.Integer()),
        sa.Column("plateau_day", sa.Integer()),
        sa.Column("total_projected_views", sa.Float()),
        sa.Column("velocity_score", sa.Float()),
        sa.Column("growth_rate_percent", sa.Float()),
        sa.Column("lower_bound", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("upper_bound", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("forecast_plot_path", sa.String(2000)),
        sa.Column("narrative", sa.Text()),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── agent_logs ────────────────────────────────────────────────────────────
    op.create_table(
        "agent_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("session_id", sa.String(255), nullable=False),
        sa.Column("iteration", sa.Integer(), default=1),
        sa.Column("agent_type", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("input_data", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("output_data", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("thinking", sa.Text()),
        sa.Column("recommendations", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("duration_ms", sa.Float()),
        sa.Column("tokens_used", sa.Integer()),
        sa.Column("llm_model", sa.String(100)),
        sa.Column("score_before", sa.Float()),
        sa.Column("score_after", sa.Float()),
        sa.Column("error_message", sa.Text()),
        sa.Column("retry_count", sa.Integer(), default=0),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_logs_asset_id", "agent_logs", ["asset_id"])
    op.create_index("ix_agent_logs_session_id", "agent_logs", ["session_id"])

    # ── publications ──────────────────────────────────────────────────────────
    op.create_table(
        "publications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("asset_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("assets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("status", sa.String(50), default="queued"),
        sa.Column("platform_video_id", sa.String(500)),
        sa.Column("platform_url", sa.String(2000)),
        sa.Column("title", sa.String(1000)),
        sa.Column("description", sa.Text()),
        sa.Column("tags", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("thumbnail_path", sa.String(2000)),
        sa.Column("virality_score_at_publish", sa.Float()),
        sa.Column("carag_iterations", sa.Integer()),
        sa.Column("views_count", sa.Integer()),
        sa.Column("likes_count", sa.Integer()),
        sa.Column("comments_count", sa.Integer()),
        sa.Column("shares_count", sa.Integer()),
        sa.Column("watch_time_hours", sa.Float()),
        sa.Column("ctr_percent", sa.Float()),
        sa.Column("platform_response", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("error_message", sa.Text()),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("published_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── model_metrics ─────────────────────────────────────────────────────────
    op.create_table(
        "model_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mlflow_run_id", sa.String(255), unique=True),
        sa.Column("mlflow_experiment_id", sa.String(255)),
        sa.Column("model_name", sa.String(255), nullable=False),
        sa.Column("model_type", sa.String(100), nullable=False),
        sa.Column("model_version", sa.String(100)),
        sa.Column("is_champion", sa.Boolean(), default=False),
        sa.Column("accuracy", sa.Float()), sa.Column("precision", sa.Float()),
        sa.Column("recall", sa.Float()), sa.Column("f1_score", sa.Float()),
        sa.Column("roc_auc", sa.Float()), sa.Column("mae", sa.Float()),
        sa.Column("mse", sa.Float()), sa.Column("rmse", sa.Float()),
        sa.Column("mape", sa.Float()),
        sa.Column("training_samples", sa.Integer()),
        sa.Column("validation_samples", sa.Integer()),
        sa.Column("training_duration_seconds", sa.Float()),
        sa.Column("hyperparameters", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("feature_importance", postgresql.JSON(astext_type=sa.Text())),
        sa.Column("drift_score", sa.Float()),
        sa.Column("drift_detected", sa.Boolean(), default=False),
        sa.Column("leaderboard_rank", sa.Integer()),
        sa.Column("tenant_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_model_metrics_is_champion", "model_metrics", ["is_champion"])


def downgrade() -> None:
    op.drop_table("model_metrics")
    op.drop_table("publications")
    op.drop_table("agent_logs")
    op.drop_table("forecasts")
    op.drop_table("predictions")
    op.drop_table("assets")
