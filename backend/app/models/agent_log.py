"""AgentLog ORM model."""
import uuid
from enum import Enum as PyEnum

from sqlalchemy import String, ForeignKey, Enum, JSON, Text, Float, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class AgentType(str, PyEnum):
    CRITIC = "critic"
    SPECIALIST = "specialist"
    EDITOR = "editor"
    VERIFICATION = "verification"
    ORCHESTRATOR = "orchestrator"


class AgentStatus(str, PyEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"


class AgentLog(Base):
    """Logs each step of the CARAG multi-agent loop."""

    __tablename__ = "agent_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), nullable=False
    )

    # CARAG session
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    iteration: Mapped[int] = mapped_column(Integer, default=1)
    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType), nullable=False)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus), nullable=False)

    # Agent I/O
    input_data: Mapped[dict | None] = mapped_column(JSON)
    output_data: Mapped[dict | None] = mapped_column(JSON)
    thinking: Mapped[str | None] = mapped_column(Text)       # Chain-of-thought
    recommendations: Mapped[dict | None] = mapped_column(JSON)

    # Performance
    duration_ms: Mapped[float | None] = mapped_column(Float)
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    llm_model: Mapped[str | None] = mapped_column(String(100))

    # Scores before / after
    score_before: Mapped[float | None] = mapped_column(Float)
    score_after: Mapped[float | None] = mapped_column(Float)

    # Error handling
    error_message: Mapped[str | None] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)

    # Audit
    tenant_id: Mapped[str | None] = mapped_column(String(255))

    def __repr__(self) -> str:
        return (
            f"<AgentLog id={self.id} agent={self.agent_type} "
            f"session={self.session_id} iter={self.iteration}>"
        )
