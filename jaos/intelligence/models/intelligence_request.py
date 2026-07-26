"""Core request model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.intelligence_request_type import (
    IntelligenceRequestType,
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
        raise TypeError(
            f"{field_name} must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"{field_name} must contain only non-empty strings"
            )

        value = item.strip().lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class IntelligenceRequest:
    """Represents a validated high-level intelligence operation."""

    objective: str
    request_type: IntelligenceRequestType
    identity: IntelligenceIdentity
    request_id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str | None = None
    context_policy: str | None = None
    required_capabilities: tuple[str, ...] = ()
    permission_constraints: tuple[str, ...] = ()
    timeout_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize intelligence request invariants."""

        if not isinstance(self.request_id, str) or not self.request_id.strip():
            raise ValueError("request_id must be a non-empty string")

        if not isinstance(self.objective, str) or not self.objective.strip():
            raise ValueError("objective must be a non-empty string")

        if not isinstance(self.request_type, IntelligenceRequestType):
            raise TypeError(
                "request_type must be an instance of "
                "IntelligenceRequestType"
            )

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an instance of IntelligenceIdentity"
            )

        if self.session_id is not None and not isinstance(
            self.session_id,
            str,
        ):
            raise TypeError("session_id must be a string or None")

        if self.context_policy is not None and not isinstance(
            self.context_policy,
            str,
        ):
            raise TypeError("context_policy must be a string or None")

        if self.timeout_seconds is not None:
            if isinstance(self.timeout_seconds, bool) or not isinstance(
                self.timeout_seconds,
                (int, float),
            ):
                raise TypeError("timeout_seconds must be a number or None")

            if float(self.timeout_seconds) <= 0.0:
                raise ValueError(
                    "timeout_seconds must be greater than zero"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        session_id = (
            self.session_id.strip()
            if self.session_id is not None
            else None
        )
        context_policy = (
            self.context_policy.strip().lower()
            if self.context_policy is not None
            else None
        )

        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "objective", self.objective.strip())
        object.__setattr__(self, "session_id", session_id or None)
        object.__setattr__(
            self,
            "context_policy",
            context_policy or None,
        )
        object.__setattr__(
            self,
            "required_capabilities",
            _normalize_string_tuple(
                self.required_capabilities,
                "required_capabilities",
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
            "timeout_seconds",
            (
                float(self.timeout_seconds)
                if self.timeout_seconds is not None
                else None
            ),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "request_id": self.request_id,
            "objective": self.objective,
            "request_type": self.request_type.value,
            "identity": self.identity.to_dict(),
            "session_id": self.session_id,
            "context_policy": self.context_policy,
            "required_capabilities": list(
                self.required_capabilities
            ),
            "permission_constraints": list(
                self.permission_constraints
            ),
            "timeout_seconds": self.timeout_seconds,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }