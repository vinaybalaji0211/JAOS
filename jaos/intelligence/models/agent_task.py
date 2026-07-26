"""Agent task model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.agent_task_status import AgentTaskStatus
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    lowercase: bool = False,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of identifiers."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{field_name} must contain only non-empty strings"
            )

        value = item.strip()

        if lowercase:
            value = value.lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class AgentTask:
    """Represents one controlled task routed to an intelligence agent."""

    parent_request_id: str
    target_capability: str
    identity: IntelligenceIdentity
    task_input: dict[str, Any]
    task_id: str = field(default_factory=lambda: str(uuid4()))
    agent_id: str | None = None
    status: AgentTaskStatus = AgentTaskStatus.PENDING
    context_source_ids: tuple[str, ...] = ()
    permission_scope: tuple[str, ...] = ()
    deadline_at: datetime | None = None
    resource_limit_seconds: float | None = None
    delegation_depth: int = 0
    max_delegation_depth: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize agent-task invariants."""

        required_strings = {
            "task_id": self.task_id,
            "parent_request_id": self.parent_request_id,
            "target_capability": self.target_capability,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an instance of IntelligenceIdentity"
            )

        if not isinstance(self.task_input, dict):
            raise TypeError("task_input must be a dictionary")

        if self.agent_id is not None and not isinstance(
            self.agent_id,
            str,
        ):
            raise TypeError("agent_id must be a string or None")

        if not isinstance(self.status, AgentTaskStatus):
            raise TypeError(
                "status must be an instance of AgentTaskStatus"
            )

        if self.deadline_at is not None:
            if not isinstance(self.deadline_at, datetime):
                raise TypeError(
                    "deadline_at must be a datetime instance or None"
                )

            if self.deadline_at.tzinfo is None:
                raise ValueError("deadline_at must be timezone-aware")

        if self.resource_limit_seconds is not None:
            if isinstance(
                self.resource_limit_seconds,
                bool,
            ) or not isinstance(
                self.resource_limit_seconds,
                (int, float),
            ):
                raise TypeError(
                    "resource_limit_seconds must be a number or None"
                )

            if float(self.resource_limit_seconds) <= 0.0:
                raise ValueError(
                    "resource_limit_seconds must be greater than zero"
                )

        depth_fields = {
            "delegation_depth": self.delegation_depth,
            "max_delegation_depth": self.max_delegation_depth,
        }

        for field_name, value in depth_fields.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{field_name} must be an integer")

            if value < 0:
                raise ValueError(f"{field_name} cannot be negative")

        if self.delegation_depth > self.max_delegation_depth:
            raise ValueError(
                "delegation_depth cannot exceed max_delegation_depth"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if (
            self.deadline_at is not None
            and self.deadline_at <= self.created_at
        ):
            raise ValueError(
                "deadline_at must be later than created_at"
            )

        agent_id = (
            self.agent_id.strip().lower()
            if self.agent_id is not None
            else None
        )

        if self.status in {
            AgentTaskStatus.ROUTED,
            AgentTaskStatus.RUNNING,
        } and not agent_id:
            raise ValueError(
                "routed or running task must define agent_id"
            )

        object.__setattr__(self, "task_id", self.task_id.strip())
        object.__setattr__(
            self,
            "parent_request_id",
            self.parent_request_id.strip(),
        )
        object.__setattr__(
            self,
            "target_capability",
            self.target_capability.strip().lower(),
        )
        object.__setattr__(self, "task_input", dict(self.task_input))
        object.__setattr__(self, "agent_id", agent_id or None)
        object.__setattr__(
            self,
            "context_source_ids",
            _normalize_string_tuple(
                self.context_source_ids,
                "context_source_ids",
            ),
        )
        object.__setattr__(
            self,
            "permission_scope",
            _normalize_string_tuple(
                self.permission_scope,
                "permission_scope",
                lowercase=True,
            ),
        )
        object.__setattr__(
            self,
            "resource_limit_seconds",
            (
                float(self.resource_limit_seconds)
                if self.resource_limit_seconds is not None
                else None
            ),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "task_id": self.task_id,
            "parent_request_id": self.parent_request_id,
            "target_capability": self.target_capability,
            "identity": self.identity.to_dict(),
            "task_input": dict(self.task_input),
            "agent_id": self.agent_id,
            "status": self.status.value,
            "context_source_ids": list(self.context_source_ids),
            "permission_scope": list(self.permission_scope),
            "deadline_at": (
                self.deadline_at.isoformat()
                if self.deadline_at is not None
                else None
            ),
            "resource_limit_seconds": self.resource_limit_seconds,
            "delegation_depth": self.delegation_depth,
            "max_delegation_depth": self.max_delegation_depth,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }