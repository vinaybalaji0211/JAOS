"""Context item model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.context_trust_level import ContextTrustLevel
from jaos.intelligence.models.intelligence_context_type import (
    IntelligenceContextType,
)
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_permissions(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    """Normalize and deduplicate permission constraints."""

    if isinstance(values, (str, bytes)):
        raise TypeError(
            "permission_constraints must be a collection of strings"
        )

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            "permission_constraints must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "permission_constraints must contain "
                "only non-empty strings"
            )

        value = item.strip().lower()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


def _normalize_score(value: float, field_name: str) -> float:
    """Validate and normalize a score in the inclusive unit interval."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be a number")

    normalized = float(value)

    if not 0.0 <= normalized <= 1.0:
        raise ValueError(
            f"{field_name} must be between 0.0 and 1.0"
        )

    return normalized


@dataclass(frozen=True, slots=True)
class ContextItem:
    """Represents one validated item used to build intelligence context."""

    context_type: IntelligenceContextType
    content: str
    identity: IntelligenceIdentity
    source: str
    trust_level: ContextTrustLevel
    item_id: str = field(default_factory=lambda: str(uuid4()))
    relevance: float = 0.0
    importance: float = 0.5
    confidence: float = 1.0
    estimated_tokens: int = 0
    permission_constraints: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        """Validate and normalize context item invariants."""

        required_strings = {
            "item_id": self.item_id,
            "content": self.content,
            "source": self.source,
        }

        for field_name, value in required_strings.items():
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field_name} must be a non-empty string"
                )

        if not isinstance(
            self.context_type,
            IntelligenceContextType,
        ):
            raise TypeError(
                "context_type must be an instance of "
                "IntelligenceContextType"
            )

        if not isinstance(self.identity, IntelligenceIdentity):
            raise TypeError(
                "identity must be an instance of IntelligenceIdentity"
            )

        if not isinstance(self.trust_level, ContextTrustLevel):
            raise TypeError(
                "trust_level must be an instance of ContextTrustLevel"
            )

        if isinstance(self.estimated_tokens, bool) or not isinstance(
            self.estimated_tokens,
            int,
        ):
            raise TypeError("estimated_tokens must be an integer")

        if self.estimated_tokens < 0:
            raise ValueError("estimated_tokens cannot be negative")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        if self.expires_at is not None:
            if not isinstance(self.expires_at, datetime):
                raise TypeError(
                    "expires_at must be a datetime instance or None"
                )

            if self.expires_at.tzinfo is None:
                raise ValueError("expires_at must be timezone-aware")

            if self.expires_at <= self.created_at:
                raise ValueError(
                    "expires_at must be later than created_at"
                )

        object.__setattr__(self, "item_id", self.item_id.strip())
        object.__setattr__(self, "content", self.content.strip())
        object.__setattr__(self, "source", self.source.strip().lower())
        object.__setattr__(
            self,
            "relevance",
            _normalize_score(self.relevance, "relevance"),
        )
        object.__setattr__(
            self,
            "importance",
            _normalize_score(self.importance, "importance"),
        )
        object.__setattr__(
            self,
            "confidence",
            _normalize_score(self.confidence, "confidence"),
        )
        object.__setattr__(
            self,
            "permission_constraints",
            _normalize_permissions(self.permission_constraints),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "item_id": self.item_id,
            "context_type": self.context_type.value,
            "content": self.content,
            "identity": self.identity.to_dict(),
            "source": self.source,
            "trust_level": self.trust_level.value,
            "relevance": self.relevance,
            "importance": self.importance,
            "confidence": self.confidence,
            "estimated_tokens": self.estimated_tokens,
            "permission_constraints": list(
                self.permission_constraints
            ),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
            "expires_at": (
                self.expires_at.isoformat()
                if self.expires_at is not None
                else None
            ),
        }