"""Decision proposal model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.decision_confidence import (
    DecisionConfidence,
)
from jaos.intelligence.models.decision_priority import (
    DecisionPriority,
)
from jaos.intelligence.models.decision_status import (
    DecisionStatus,
)
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of non-empty strings."""

    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(f"{field_name} must be a collection of strings") from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name} must contain only non-empty strings")

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class DecisionProposal:
    """
    Represents the provider-independent output produced by
    the Decision Engine.

    A DecisionProposal evaluates a PlanProposal and determines
    whether it should proceed toward execution.
    """

    request_id: str
    identity: IntelligenceIdentity
    plan_proposal: PlanProposal
    decision_summary: str
    decision_rationale: str

    decision_id: str = field(default_factory=lambda: str(uuid4()))
    status: DecisionStatus = DecisionStatus.DRAFT
    priority: DecisionPriority = DecisionPriority.NORMAL
    confidence: DecisionConfidence = DecisionConfidence.MEDIUM
    approved: bool = False
    required_approvals: tuple[str, ...] = ()
    execution_constraints: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize proposal invariants."""

        required_strings = {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "decision_summary": self.decision_summary,
            "decision_rationale": self.decision_rationale,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError("identity must be an instance of IntelligenceIdentity")

        if not isinstance(self.plan_proposal, PlanProposal):
            raise TypeError("plan_proposal must be an instance of PlanProposal")

        if not isinstance(self.status, DecisionStatus):
            raise TypeError("status must be an instance of DecisionStatus")

        if not isinstance(self.priority, DecisionPriority):
            raise TypeError("priority must be an instance of DecisionPriority")

        if not isinstance(
            self.confidence,
            DecisionConfidence,
        ):
            raise TypeError("confidence must be an instance of DecisionConfidence")

        if not isinstance(self.approved, bool):
            raise TypeError("approved must be a boolean")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        object.__setattr__(
            self,
            "decision_id",
            self.decision_id.strip(),
        )

        object.__setattr__(
            self,
            "request_id",
            self.request_id.strip(),
        )

        object.__setattr__(
            self,
            "decision_summary",
            self.decision_summary.strip(),
        )

        object.__setattr__(
            self,
            "decision_rationale",
            self.decision_rationale.strip(),
        )

        object.__setattr__(
            self,
            "required_approvals",
            _normalize_string_tuple(
                self.required_approvals,
                "required_approvals",
            ),
        )

        object.__setattr__(
            self,
            "execution_constraints",
            _normalize_string_tuple(
                self.execution_constraints,
                "execution_constraints",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

    @property
    def planning_id(self) -> str:
        """Return the originating planning identifier."""

        return self.plan_proposal.planning_id

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "planning_id": self.planning_id,
            "identity": self.identity.to_dict(),
            "plan_proposal": self.plan_proposal.to_dict(),
            "status": self.status.value,
            "priority": self.priority.value,
            "confidence": self.confidence.value,
            "approved": self.approved,
            "decision_summary": self.decision_summary,
            "decision_rationale": self.decision_rationale,
            "required_approvals": list(self.required_approvals),
            "execution_constraints": list(self.execution_constraints),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }
