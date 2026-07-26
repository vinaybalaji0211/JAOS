"""Agent result model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.agent_task_status import AgentTaskStatus


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


_TERMINAL_STATUSES = {
    AgentTaskStatus.SUCCEEDED,
    AgentTaskStatus.FAILED,
    AgentTaskStatus.REJECTED,
    AgentTaskStatus.CANCELLED,
}


@dataclass(frozen=True, slots=True)
class AgentResult:
    """Represents the validated terminal result of an agent task."""

    task_id: str
    agent_id: str
    status: AgentTaskStatus
    result_id: str = field(default_factory=lambda: str(uuid4()))
    output: str | None = None
    structured_output: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    error_code: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    completed_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize agent-result invariants."""

        required_strings = {
            "result_id": self.result_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(self.status, AgentTaskStatus):
            raise TypeError(
                "status must be an instance of AgentTaskStatus"
            )

        if self.status not in _TERMINAL_STATUSES:
            raise ValueError(
                "agent result status must be terminal"
            )

        if self.output is not None and not isinstance(self.output, str):
            raise TypeError("output must be a string or None")

        if not isinstance(self.structured_output, dict):
            raise TypeError(
                "structured_output must be a dictionary"
            )

        if isinstance(self.confidence, bool) or not isinstance(
            self.confidence,
            (int, float),
        ):
            raise TypeError("confidence must be a number")

        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0"
            )

        optional_strings = {
            "error_code": self.error_code,
            "error_message": self.error_message,
        }

        for field_name, value in optional_strings.items():
            if value is not None and not isinstance(value, str):
                raise TypeError(
                    f"{field_name} must be a string or None"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.completed_at, datetime):
            raise TypeError("completed_at must be a datetime instance")

        if self.completed_at.tzinfo is None:
            raise ValueError("completed_at must be timezone-aware")

        output = self.output.strip() if self.output is not None else None
        error_code = (
            self.error_code.strip().lower()
            if self.error_code is not None
            else None
        )
        error_message = (
            self.error_message.strip()
            if self.error_message is not None
            else None
        )

        if (
            self.status is AgentTaskStatus.SUCCEEDED
            and not output
            and not self.structured_output
        ):
            raise ValueError(
                "successful agent result must define output "
                "or structured_output"
            )

        if (
            self.status is not AgentTaskStatus.SUCCEEDED
            and not error_message
        ):
            raise ValueError(
                "unsuccessful agent result must define error_message"
            )

        object.__setattr__(self, "result_id", self.result_id.strip())
        object.__setattr__(self, "task_id", self.task_id.strip())
        object.__setattr__(
            self,
            "agent_id",
            self.agent_id.strip().lower(),
        )
        object.__setattr__(self, "output", output or None)
        object.__setattr__(
            self,
            "structured_output",
            dict(self.structured_output),
        )
        object.__setattr__(self, "confidence", float(self.confidence))
        object.__setattr__(self, "error_code", error_code or None)
        object.__setattr__(self, "error_message", error_message or None)
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "result_id": self.result_id,
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "status": self.status.value,
            "output": self.output,
            "structured_output": dict(self.structured_output),
            "confidence": self.confidence,
            "error_code": self.error_code,
            "error_message": self.error_message,
            "metadata": dict(self.metadata),
            "completed_at": self.completed_at.isoformat(),
        }