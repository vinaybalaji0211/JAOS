"""Reasoning assumption model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def _normalize_identifier_tuple(
    values: tuple[str, ...],
) -> tuple[str, ...]:
    """Normalize and deduplicate context-source identifiers."""

    if isinstance(values, (str, bytes)):
        raise TypeError(
            "source_context_ids must be a collection of strings"
        )

    try:
        items = tuple(values)
    except TypeError as exc:
        raise TypeError(
            "source_context_ids must be a collection of strings"
        ) from exc

    normalized: list[str] = []

    for item in items:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "source_context_ids must contain "
                "only non-empty strings"
            )

        value = item.strip()

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ReasoningAssumption:
    """Represents one explicit assumption in a reasoning result."""

    statement: str
    confidence: float
    assumption_id: str = field(default_factory=lambda: str(uuid4()))
    source_context_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate and normalize reasoning-assumption invariants."""

        if (
            not isinstance(self.assumption_id, str)
            or not self.assumption_id.strip()
        ):
            raise ValueError(
                "assumption_id must be a non-empty string"
            )

        if not isinstance(self.statement, str) or not self.statement.strip():
            raise ValueError("statement must be a non-empty string")

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

        object.__setattr__(
            self,
            "assumption_id",
            self.assumption_id.strip(),
        )
        object.__setattr__(self, "statement", self.statement.strip())
        object.__setattr__(self, "confidence", float(self.confidence))
        object.__setattr__(
            self,
            "source_context_ids",
            _normalize_identifier_tuple(self.source_context_ids),
        )
        object.__setattr__(self, "metadata", dict(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "assumption_id": self.assumption_id,
            "statement": self.statement,
            "confidence": self.confidence,
            "source_context_ids": list(self.source_context_ids),
            "metadata": dict(self.metadata),
        }