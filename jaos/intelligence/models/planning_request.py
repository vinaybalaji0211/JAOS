"""Planning request model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.context_bundle import ContextBundle
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.reasoning_result import ReasoningResult


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
class PlanningRequest:
    """Represents a validated intelligent-planning request."""

    request_id: str
    goal: str
    identity: IntelligenceIdentity
    reasoning_result: ReasoningResult | None = None
    context_bundle: ContextBundle | None = None
    planning_id: str = field(default_factory=lambda: str(uuid4()))
    constraints: tuple[str, ...] = ()
    available_capabilities: tuple[str, ...] = ()
    permission_constraints: tuple[str, ...] = ()
    risk_policy: str = "default"
    success_criteria: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize planning-request invariants."""

        required_strings = {
            "planning_id": self.planning_id,
            "request_id": self.request_id,
            "goal": self.goal,
            "risk_policy": self.risk_policy,
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

        if self.reasoning_result is not None and not isinstance(
            self.reasoning_result,
            ReasoningResult,
        ):
            raise TypeError(
                "reasoning_result must be a ReasoningResult or None"
            )

        if self.context_bundle is not None and not isinstance(
            self.context_bundle,
            ContextBundle,
        ):
            raise TypeError(
                "context_bundle must be a ContextBundle or None"
            )

        if (
            self.reasoning_result is None
            and self.context_bundle is None
        ):
            raise ValueError(
                "planning request requires reasoning_result "
                "or context_bundle"
            )

        request_id = self.request_id.strip()

        if (
            self.reasoning_result is not None
            and self.reasoning_result.request_id != request_id
        ):
            raise ValueError(
                "reasoning_result request_id must match request_id"
            )

        if (
            self.context_bundle is not None
            and self.context_bundle.request_id != request_id
        ):
            raise ValueError(
                "context_bundle request_id must match request_id"
            )

        if (
            self.context_bundle is not None
            and self.context_bundle.identity != self.identity
        ):
            raise ValueError(
                "context_bundle identity must match identity"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        object.__setattr__(
            self,
            "planning_id",
            self.planning_id.strip(),
        )
        object.__setattr__(self, "request_id", request_id)
        object.__setattr__(self, "goal", self.goal.strip())
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
            "available_capabilities",
            _normalize_string_tuple(
                self.available_capabilities,
                "available_capabilities",
                lowercase=True,
            ),
        )
        object.__setattr__(
            self,
            "permission_constraints",
            _normalize_string_tuple(
                self.permission_constraints,
                "permission_constraints",
                lowercase=True,
            ),
        )
        object.__setattr__(
            self,
            "risk_policy",
            self.risk_policy.strip().lower(),
        )
        object.__setattr__(
            self,
            "success_criteria",
            _normalize_string_tuple(
                self.success_criteria,
                "success_criteria",
            ),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "planning_id": self.planning_id,
            "request_id": self.request_id,
            "goal": self.goal,
            "identity": self.identity.to_dict(),
            "reasoning_result": (
                self.reasoning_result.to_dict()
                if self.reasoning_result is not None
                else None
            ),
            "context_bundle": (
                self.context_bundle.to_dict()
                if self.context_bundle is not None
                else None
            ),
            "constraints": list(self.constraints),
            "available_capabilities": list(
                self.available_capabilities
            ),
            "permission_constraints": list(
                self.permission_constraints
            ),
            "risk_policy": self.risk_policy,
            "success_criteria": list(self.success_criteria),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }