"""Execution proposal model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.intelligence_identity import IntelligenceIdentity
from jaos.intelligence.models.proposal_status import ProposalStatus
from jaos.intelligence.models.risk_level import RiskLevel


def _normalize_required_text(value: str, field_name: str) -> str:
    """Validate and normalize a required text field."""

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()

    if not normalized:
        raise ValueError(f"{field_name} must not be empty")

    return normalized


def _normalize_optional_text(
    value: str | None,
    field_name: str,
) -> str | None:
    """Validate and normalize an optional text field."""

    if value is None:
        return None

    return _normalize_required_text(value, field_name)


def _normalize_text_collection(
    values: tuple[str, ...],
    field_name: str,
    *,
    lowercase: bool = False,
    required: bool = False,
) -> tuple[str, ...]:
    """Validate, normalize, and deduplicate a text collection."""

    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list of strings")

    normalized_values: list[str] = []
    seen: set[str] = set()

    for value in values:
        normalized = _normalize_required_text(value, field_name)

        if lowercase:
            normalized = normalized.lower()

        if normalized not in seen:
            seen.add(normalized)
            normalized_values.append(normalized)

    if required and not normalized_values:
        raise ValueError(f"{field_name} must contain at least one value")

    return tuple(normalized_values)


def _normalize_datetime(value: datetime, field_name: str) -> datetime:
    """Validate and normalize an aware datetime to UTC."""

    if not isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a datetime")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")

    return value.astimezone(timezone.utc)


@dataclass(frozen=True, slots=True)
class ExecutionProposal:
    """
    Describes a proposed executable action without executing it.

    This contract preserves the boundary between intelligence and execution.
    The Intelligence Platform may describe an action, required capability,
    permissions, risk, and expected result, but only the Executive and Tool
    Platforms may authorize and perform the action.
    """

    source_request_id: str
    action_description: str
    required_capability: str
    identity: IntelligenceIdentity
    structured_inputs: dict[str, Any]
    expected_result: str
    success_criteria: tuple[str, ...]
    proposal_id: str = field(default_factory=lambda: str(uuid4()))
    plan_proposal_id: str | None = None
    agent_task_id: str | None = None
    suggested_tool_category: str | None = None
    permission_requirements: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.NONE
    recovery_guidance: tuple[str, ...] = ()
    status: ProposalStatus = ProposalStatus.DRAFT
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """Validate and normalize execution proposal invariants."""

        object.__setattr__(
            self,
            "source_request_id",
            _normalize_required_text(
                self.source_request_id,
                "source_request_id",
            ),
        )
        object.__setattr__(
            self,
            "action_description",
            _normalize_required_text(
                self.action_description,
                "action_description",
            ),
        )
        object.__setattr__(
            self,
            "required_capability",
            _normalize_required_text(
                self.required_capability,
                "required_capability",
            ).lower(),
        )

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an instance of IntelligenceIdentity"
            )

        if not isinstance(self.structured_inputs, dict):
            raise TypeError("structured_inputs must be a dictionary")

        object.__setattr__(
            self,
            "structured_inputs",
            dict(self.structured_inputs),
        )
        object.__setattr__(
            self,
            "expected_result",
            _normalize_required_text(
                self.expected_result,
                "expected_result",
            ),
        )
        object.__setattr__(
            self,
            "success_criteria",
            _normalize_text_collection(
                self.success_criteria,
                "success_criteria",
                required=True,
            ),
        )
        object.__setattr__(
            self,
            "proposal_id",
            _normalize_required_text(
                self.proposal_id,
                "proposal_id",
            ),
        )
        object.__setattr__(
            self,
            "plan_proposal_id",
            _normalize_optional_text(
                self.plan_proposal_id,
                "plan_proposal_id",
            ),
        )
        object.__setattr__(
            self,
            "agent_task_id",
            _normalize_optional_text(
                self.agent_task_id,
                "agent_task_id",
            ),
        )

        suggested_tool_category = _normalize_optional_text(
            self.suggested_tool_category,
            "suggested_tool_category",
        )

        if suggested_tool_category is not None:
            suggested_tool_category = suggested_tool_category.lower()

        object.__setattr__(
            self,
            "suggested_tool_category",
            suggested_tool_category,
        )
        object.__setattr__(
            self,
            "permission_requirements",
            _normalize_text_collection(
                self.permission_requirements,
                "permission_requirements",
                lowercase=True,
            ),
        )

        if not isinstance(self.risk_level, RiskLevel):
            raise TypeError("risk_level must be an instance of RiskLevel")

        object.__setattr__(
            self,
            "recovery_guidance",
            _normalize_text_collection(
                self.recovery_guidance,
                "recovery_guidance",
            ),
        )

        if not isinstance(self.status, ProposalStatus):
            raise TypeError("status must be an instance of ProposalStatus")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        object.__setattr__(self, "metadata", dict(self.metadata))
        object.__setattr__(
            self,
            "created_at",
            _normalize_datetime(self.created_at, "created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe representation of the proposal."""

        return {
            "proposal_id": self.proposal_id,
            "source_request_id": self.source_request_id,
            "plan_proposal_id": self.plan_proposal_id,
            "agent_task_id": self.agent_task_id,
            "action_description": self.action_description,
            "required_capability": self.required_capability,
            "identity": self.identity.to_dict(),
            "structured_inputs": dict(self.structured_inputs),
            "suggested_tool_category": self.suggested_tool_category,
            "expected_result": self.expected_result,
            "success_criteria": list(self.success_criteria),
            "permission_requirements": list(
                self.permission_requirements
            ),
            "risk_level": self.risk_level.value,
            "recovery_guidance": list(self.recovery_guidance),
            "status": self.status.value,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }