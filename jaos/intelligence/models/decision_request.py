"""Decision request model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.decision_priority import (
    DecisionPriority,
)
from jaos.intelligence.models.decision_strategy import (
    DecisionStrategy,
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


@dataclass(frozen=True, slots=True)
class DecisionRequest:
    """
    Represents a provider-independent request to evaluate
    a proposed execution plan.

    A DecisionRequest is created after the Planning Engine
    has successfully generated a validated PlanProposal.
    The Decision Engine evaluates the proposal and determines
    whether it should proceed to execution.
    """

    identity: IntelligenceIdentity
    plan_proposal: PlanProposal

    request_id: str = field(default_factory=lambda: str(uuid4()))
    decision_strategy: DecisionStrategy = DecisionStrategy.ADAPTIVE
    priority: DecisionPriority = DecisionPriority.NORMAL
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize request invariants."""

        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise ValueError("request_id must be a non-empty string")

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError("identity must be an instance of IntelligenceIdentity")

        if not isinstance(self.plan_proposal, PlanProposal):
            raise TypeError("plan_proposal must be an instance of PlanProposal")

        if not isinstance(
            self.decision_strategy,
            DecisionStrategy,
        ):
            raise TypeError("decision_strategy must be an instance of DecisionStrategy")

        if not isinstance(
            self.priority,
            DecisionPriority,
        ):
            raise TypeError("priority must be an instance of DecisionPriority")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        object.__setattr__(
            self,
            "request_id",
            self.request_id.strip(),
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
            "request_id": self.request_id,
            "planning_id": self.planning_id,
            "identity": self.identity.to_dict(),
            "plan_proposal": self.plan_proposal.to_dict(),
            "decision_strategy": self.decision_strategy.value,
            "priority": self.priority.value,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }
