"""Planning request model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.planning_configuration import (
    PlanningConfiguration,
)
from jaos.intelligence.models.reasoning_result import (
    ReasoningResult,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_string_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize, validate, and deduplicate a tuple of strings."""

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

        value = item.strip().lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class PlanningRequest:
    """
    Represents a validated planning request.

    A PlanningRequest encapsulates all validated cognitive
    understanding and operational planning controls required
    by a PlanningEngine to generate a deterministic plan.

    This model adheres to:

    • AP-012 — Cognitive Context Isolation
    • AP-013 — Deterministic Planning Inputs
    • AP-015 — Cognitive Artifact Completeness
    • AP-016 — Planning Configuration Isolation
    • AP-017 — Planner Policy Independence
    • AP-019 — Trusted Domain Artifacts
    """

    request_id: str

    identity: IntelligenceIdentity

    goal: str

    reasoning_result: ReasoningResult

    planning_id: str = field(default_factory=lambda: str(uuid4()))

    configuration: PlanningConfiguration = field(default_factory=PlanningConfiguration)

    constraints: tuple[str, ...] = ()

    permission_constraints: tuple[str, ...] = ()

    success_criteria: tuple[str, ...] = ()

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize planning request."""

        required_strings = {
            "request_id": self.request_id,
            "planning_id": self.planning_id,
            "goal": self.goal,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")

        if not isinstance(
            self.identity,
            IntelligenceIdentity,
        ):
            raise TypeError("identity must be an instance of " "IntelligenceIdentity")

        if not isinstance(
            self.reasoning_result,
            ReasoningResult,
        ):
            raise TypeError(
                "reasoning_result must be an instance of " "ReasoningResult"
            )

        if not isinstance(
            self.configuration,
            PlanningConfiguration,
        ):
            raise TypeError(
                "configuration must be an instance of " "PlanningConfiguration"
            )

        if self.reasoning_result.request_id != self.request_id.strip():
            raise ValueError("reasoning_result request_id must " "match request_id")

        if not isinstance(
            self.metadata,
            dict,
        ):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(
            self.created_at,
            datetime,
        ):
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
            "planning_id",
            self.planning_id.strip(),
        )

        object.__setattr__(
            self,
            "goal",
            self.goal.strip(),
        )

        object.__setattr__(
            self,
            "constraints",
            _normalize_string_tuple(
                self.constraints,
                "constraints",
            ),
        )

        object.__setattr__(
            self,
            "permission_constraints",
            _normalize_string_tuple(
                self.permission_constraints,
                "permission_constraints",
            ),
        )

        object.__setattr__(
            self,
            "success_criteria",
            _normalize_string_tuple(
                self.success_criteria,
                "success_criteria",
            ),
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "request_id": self.request_id,
            "planning_id": self.planning_id,
            "identity": self.identity.to_dict(),
            "goal": self.goal,
            "reasoning_result": (self.reasoning_result.to_dict()),
            "configuration": (self.configuration.to_dict()),
            "constraints": list(self.constraints),
            "permission_constraints": list(self.permission_constraints),
            "success_criteria": list(self.success_criteria),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }
