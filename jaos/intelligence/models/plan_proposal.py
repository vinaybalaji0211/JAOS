"""Plan proposal model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.proposal_status import ProposalStatus
from jaos.intelligence.models.proposed_plan_step import ProposedPlanStep
from jaos.intelligence.models.risk_level import RiskLevel

_RISK_ORDER = {
    RiskLevel.NONE: 0,
    RiskLevel.LOW: 1,
    RiskLevel.MEDIUM: 2,
    RiskLevel.HIGH: 3,
    RiskLevel.CRITICAL: 4,
}


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
    *,
    lowercase: bool = False,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of non-empty strings."""

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
class PlanProposal:
    """Represents a validated non-authoritative intelligent plan."""

    planning_id: str
    request_id: str
    goal: str
    identity: IntelligenceIdentity
    steps: tuple[ProposedPlanStep, ...]
    expected_outcomes: tuple[str, ...]
    success_criteria: tuple[str, ...]
    proposal_id: str = field(default_factory=lambda: str(uuid4()))
    status: ProposalStatus = ProposalStatus.DRAFT
    reasoning_result_id: str | None = None
    required_capabilities: tuple[str, ...] = ()
    permission_requirements: tuple[str, ...] = ()
    failure_conditions: tuple[str, ...] = ()
    recovery_guidance: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.NONE
    confidence: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize plan-proposal invariants."""

        required_strings = {
            "proposal_id": self.proposal_id,
            "planning_id": self.planning_id,
            "request_id": self.request_id,
            "goal": self.goal,
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

        try:
            steps = tuple(self.steps)
        except TypeError as exc:
            raise TypeError(
                "steps must be a collection of ProposedPlanStep instances"
            ) from exc

        if not steps:
            raise ValueError("plan proposal must contain at least one step")

        for step in steps:
            if not isinstance(step, ProposedPlanStep):
                raise TypeError(
                    "steps must contain only ProposedPlanStep instances"
                )

        step_ids = tuple(step.step_id for step in steps)
        step_orders = tuple(step.step_order for step in steps)

        if len(step_ids) != len(set(step_ids)):
            raise ValueError("proposed step IDs must be unique")

        if step_orders != tuple(range(1, len(steps) + 1)):
            raise ValueError(
                "proposed steps must be ordered consecutively from one"
            )

        step_order_by_id = {
            step.step_id: step.step_order
            for step in steps
        }

        for step in steps:
            for dependency in step.dependencies:
                if dependency not in step_order_by_id:
                    raise ValueError(
                        "step dependencies must reference proposal steps"
                    )

                if step_order_by_id[dependency] >= step.step_order:
                    raise ValueError(
                        "step dependencies must reference earlier steps"
                    )

        if not isinstance(self.status, ProposalStatus):
            raise TypeError(
                "status must be an instance of ProposalStatus"
            )

        if (
            self.reasoning_result_id is not None
            and not isinstance(self.reasoning_result_id, str)
        ):
            raise TypeError(
                "reasoning_result_id must be a string or None"
            )

        if not isinstance(self.risk_level, RiskLevel):
            raise TypeError(
                "risk_level must be an instance of RiskLevel"
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

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        expected_outcomes = _normalize_string_tuple(
            self.expected_outcomes,
            "expected_outcomes",
        )
        success_criteria = _normalize_string_tuple(
            self.success_criteria,
            "success_criteria",
        )

        if not expected_outcomes:
            raise ValueError(
                "expected_outcomes must contain at least one value"
            )

        if not success_criteria:
            raise ValueError(
                "success_criteria must contain at least one value"
            )

        provided_capabilities = _normalize_string_tuple(
            self.required_capabilities,
            "required_capabilities",
            lowercase=True,
        )
        step_capabilities = tuple(
            step.required_capability
            for step in steps
        )
        required_capabilities = tuple(
            dict.fromkeys(
                provided_capabilities + step_capabilities
            )
        )

        provided_permissions = _normalize_string_tuple(
            self.permission_requirements,
            "permission_requirements",
            lowercase=True,
        )
        step_permissions = tuple(
            permission
            for step in steps
            for permission in step.permission_requirements
        )
        permission_requirements = tuple(
            dict.fromkeys(
                provided_permissions + step_permissions
            )
        )

        highest_risk = self.risk_level

        for step in steps:
            if _RISK_ORDER[step.risk_level] > _RISK_ORDER[highest_risk]:
                highest_risk = step.risk_level

        reasoning_result_id = (
            self.reasoning_result_id.strip()
            if self.reasoning_result_id is not None
            else None
        )

        object.__setattr__(
            self,
            "proposal_id",
            self.proposal_id.strip(),
        )
        object.__setattr__(
            self,
            "planning_id",
            self.planning_id.strip(),
        )
        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "goal", self.goal.strip())
        object.__setattr__(self, "steps", steps)
        object.__setattr__(
            self,
            "reasoning_result_id",
            reasoning_result_id or None,
        )
        object.__setattr__(
            self,
            "required_capabilities",
            required_capabilities,
        )
        object.__setattr__(
            self,
            "permission_requirements",
            permission_requirements,
        )
        object.__setattr__(
            self,
            "expected_outcomes",
            expected_outcomes,
        )
        object.__setattr__(
            self,
            "success_criteria",
            success_criteria,
        )
        object.__setattr__(
            self,
            "failure_conditions",
            _normalize_string_tuple(
                self.failure_conditions,
                "failure_conditions",
            ),
        )
        object.__setattr__(
            self,
            "recovery_guidance",
            _normalize_string_tuple(
                self.recovery_guidance,
                "recovery_guidance",
            ),
        )
        object.__setattr__(
            self,
            "risks",
            _normalize_string_tuple(self.risks, "risks"),
        )
        object.__setattr__(self, "risk_level", highest_risk)
        object.__setattr__(self, "confidence", float(self.confidence))
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "proposal_id": self.proposal_id,
            "planning_id": self.planning_id,
            "request_id": self.request_id,
            "goal": self.goal,
            "identity": self.identity.to_dict(),
            "status": self.status.value,
            "reasoning_result_id": self.reasoning_result_id,
            "steps": [step.to_dict() for step in self.steps],
            "required_capabilities": list(
                self.required_capabilities
            ),
            "permission_requirements": list(
                self.permission_requirements
            ),
            "expected_outcomes": list(self.expected_outcomes),
            "success_criteria": list(self.success_criteria),
            "failure_conditions": list(self.failure_conditions),
            "recovery_guidance": list(self.recovery_guidance),
            "risks": list(self.risks),
            "risk_level": self.risk_level.value,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }