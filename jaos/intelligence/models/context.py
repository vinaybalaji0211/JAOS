"""Core context model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from jaos.intelligence.models.context_priority import ContextPriority
from jaos.intelligence.models.context_type import ContextType
from jaos.intelligence.models.context_validation_state import (
    ContextValidationState,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class Context:
    """
    Represents a validated piece of contextual information used during
    reasoning, planning, and decision generation.
    """

    context_type: ContextType
    source: str
    content: Any

    context_id: str = field(default_factory=lambda: str(uuid4()))

    priority: ContextPriority = ContextPriority.NORMAL

    confidence: float = 1.0

    validation_state: ContextValidationState = (
        ContextValidationState.UNKNOWN
    )

    freshness_seconds: float | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        """Validate and normalize the context model."""

        try:
            UUID(self.context_id)
        except Exception as exc:
            raise ValueError(
                "context_id must be a valid UUID"
            ) from exc

        if not isinstance(self.context_type, ContextType):
            raise TypeError(
                "context_type must be ContextType"
            )

        if not isinstance(self.priority, ContextPriority):
            raise TypeError(
                "priority must be ContextPriority"
            )

        if not isinstance(
            self.validation_state,
            ContextValidationState,
        ):
            raise TypeError(
                "validation_state must be "
                "ContextValidationState"
            )

        if (
            not isinstance(self.source, str)
            or not self.source.strip()
        ):
            raise ValueError(
                "source must be a non-empty string"
            )

        if isinstance(self.confidence, bool) or not isinstance(
            self.confidence,
            (int, float),
        ):
            raise TypeError(
                "confidence must be numeric"
            )

        confidence = float(self.confidence)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence must be between "
                "0.0 and 1.0"
            )

        if self.freshness_seconds is not None:
            if isinstance(
                self.freshness_seconds,
                bool,
            ) or not isinstance(
                self.freshness_seconds,
                (int, float),
            ):
                raise TypeError(
                    "freshness_seconds must be numeric"
                )

            if self.freshness_seconds < 0:
                raise ValueError(
                    "freshness_seconds cannot be negative"
                )

        if not isinstance(self.metadata, dict):
            raise TypeError(
                "metadata must be a dictionary"
            )

        if not isinstance(self.created_at, datetime):
            raise TypeError(
                "created_at must be datetime"
            )

        if self.created_at.tzinfo is None:
            raise ValueError(
                "created_at must be timezone-aware"
            )

        object.__setattr__(
            self,
            "source",
            self.source.strip().lower(),
        )

        object.__setattr__(
            self,
            "confidence",
            confidence,
        )

        object.__setattr__(
            self,
            "metadata",
            dict(self.metadata),
        )

        if self.freshness_seconds is not None:
            object.__setattr__(
                self,
                "freshness_seconds",
                float(self.freshness_seconds),
            )

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary."""

        return {
            "context_id": self.context_id,
            "context_type": self.context_type.value,
            "source": self.source,
            "content": self.content,
            "priority": int(self.priority),
            "confidence": self.confidence,
            "validation_state": self.validation_state.value,
            "freshness_seconds": self.freshness_seconds,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }