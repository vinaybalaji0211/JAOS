"""Reasoning request model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.context_bundle import ContextBundle


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_constraints(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    """Normalize and deduplicate reasoning constraints."""

    if isinstance(values, (str, bytes)):
        raise TypeError("constraints must be a collection of strings")

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            "constraints must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "constraints must contain only non-empty strings"
            )

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ReasoningRequest:
    """Represents a validated structured-reasoning request."""

    request_id: str
    objective: str
    context_bundle: ContextBundle
    reasoning_id: str = field(default_factory=lambda: str(uuid4()))
    constraints: tuple[str, ...] = ()
    required_output_type: str = "reasoning_result"
    risk_policy: str = "default"
    max_alternatives: int = 3
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize reasoning-request invariants."""

        required_strings = {
            "reasoning_id": self.reasoning_id,
            "request_id": self.request_id,
            "objective": self.objective,
            "required_output_type": self.required_output_type,
            "risk_policy": self.risk_policy,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(self.context_bundle, ContextBundle):
            raise TypeError(
                "context_bundle must be an instance of ContextBundle"
            )

        if (
            self.context_bundle.request_id.strip()
            != self.request_id.strip()
        ):
            raise ValueError(
                "context_bundle request_id must match request_id"
            )

        if isinstance(self.max_alternatives, bool) or not isinstance(
            self.max_alternatives,
            int,
        ):
            raise TypeError("max_alternatives must be an integer")

        if self.max_alternatives <= 0:
            raise ValueError(
                "max_alternatives must be greater than zero"
            )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        object.__setattr__(
            self,
            "reasoning_id",
            self.reasoning_id.strip(),
        )
        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "objective", self.objective.strip())
        object.__setattr__(
            self,
            "constraints",
            _normalize_constraints(self.constraints),
        )
        object.__setattr__(
            self,
            "required_output_type",
            self.required_output_type.strip().lower(),
        )
        object.__setattr__(
            self,
            "risk_policy",
            self.risk_policy.strip().lower(),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "reasoning_id": self.reasoning_id,
            "request_id": self.request_id,
            "objective": self.objective,
            "context_bundle": self.context_bundle.to_dict(),
            "constraints": list(self.constraints),
            "required_output_type": self.required_output_type,
            "risk_policy": self.risk_policy,
            "max_alternatives": self.max_alternatives,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }