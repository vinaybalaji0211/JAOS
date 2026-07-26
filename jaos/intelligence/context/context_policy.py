"""Context policy definitions for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from jaos.intelligence.exceptions import IntelligenceContextError
from jaos.intelligence.models import (
    ContextTrustLevel,
    IntelligenceContextType,
)


def _validate_positive_integer(value: int, field_name: str) -> int:
    """Validate a positive integer."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")

    return value


def _validate_score(value: float, field_name: str) -> float:
    """Validate a score between zero and one."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")

    normalized = float(value)

    if not 0.0 <= normalized <= 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0")

    return normalized


def _normalize_enum_collection(
    values: tuple[Any, ...] | list[Any],
    enum_type: type,
    field_name: str,
) -> tuple[Any, ...]:
    """Normalize and deduplicate enum values."""

    if not isinstance(values, (tuple, list)):
        raise TypeError(f"{field_name} must be a tuple or list")

    normalized_values: list[Any] = []
    seen: set[Any] = set()

    for value in values:
        if isinstance(value, enum_type):
            normalized = value
        elif isinstance(value, str):
            try:
                normalized = enum_type(value.strip().lower())
            except ValueError as exc:
                raise ValueError(
                    f"invalid value for {field_name}: {value}"
                ) from exc
        else:
            raise TypeError(
                f"{field_name} values must be {enum_type.__name__} "
                "instances or strings"
            )

        if normalized not in seen:
            seen.add(normalized)
            normalized_values.append(normalized)

    if not normalized_values:
        raise ValueError(f"{field_name} must not be empty")

    return tuple(normalized_values)


@dataclass(frozen=True, slots=True)
class ContextPolicy:
    """Validated rules controlling context assembly."""

    max_tokens: int = 4096
    max_items: int = 64
    minimum_relevance: float = 0.0
    minimum_importance: float = 0.0
    allowed_context_types: tuple[IntelligenceContextType, ...] = field(
        default_factory=lambda: tuple(IntelligenceContextType)
    )
    allowed_trust_levels: tuple[ContextTrustLevel, ...] = field(
        default_factory=lambda: tuple(ContextTrustLevel)
    )
    include_expired: bool = False
    fail_on_source_error: bool = False
    fail_on_conflict: bool = False
    deduplicate: bool = True

    def __post_init__(self) -> None:
        """Validate and normalize policy values."""

        object.__setattr__(
            self,
            "max_tokens",
            _validate_positive_integer(self.max_tokens, "max_tokens"),
        )
        object.__setattr__(
            self,
            "max_items",
            _validate_positive_integer(self.max_items, "max_items"),
        )
        object.__setattr__(
            self,
            "minimum_relevance",
            _validate_score(
                self.minimum_relevance,
                "minimum_relevance",
            ),
        )
        object.__setattr__(
            self,
            "minimum_importance",
            _validate_score(
                self.minimum_importance,
                "minimum_importance",
            ),
        )
        object.__setattr__(
            self,
            "allowed_context_types",
            _normalize_enum_collection(
                self.allowed_context_types,
                IntelligenceContextType,
                "allowed_context_types",
            ),
        )
        object.__setattr__(
            self,
            "allowed_trust_levels",
            _normalize_enum_collection(
                self.allowed_trust_levels,
                ContextTrustLevel,
                "allowed_trust_levels",
            ),
        )

        for field_name in (
            "include_expired",
            "fail_on_source_error",
            "fail_on_conflict",
            "deduplicate",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be a boolean")

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, Any] | None,
    ) -> ContextPolicy:
        """Create a policy from a request policy mapping."""

        if values is None:
            return cls()

        if not isinstance(values, Mapping):
            raise TypeError("context policy must be a mapping")

        allowed_fields = {
            "max_tokens",
            "max_items",
            "minimum_relevance",
            "minimum_importance",
            "allowed_context_types",
            "allowed_trust_levels",
            "include_expired",
            "fail_on_source_error",
            "fail_on_conflict",
            "deduplicate",
        }
        unknown_fields = set(values) - allowed_fields

        if unknown_fields:
            names = ", ".join(sorted(str(name) for name in unknown_fields))
            raise IntelligenceContextError(
                f"unsupported context policy fields: {names}",
                details={"unknown_fields": sorted(unknown_fields)},
            )

        return cls(**dict(values))

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe policy representation."""

        return {
            "max_tokens": self.max_tokens,
            "max_items": self.max_items,
            "minimum_relevance": self.minimum_relevance,
            "minimum_importance": self.minimum_importance,
            "allowed_context_types": [
                context_type.value
                for context_type in self.allowed_context_types
            ],
            "allowed_trust_levels": [
                trust_level.value
                for trust_level in self.allowed_trust_levels
            ],
            "include_expired": self.include_expired,
            "fail_on_source_error": self.fail_on_source_error,
            "fail_on_conflict": self.fail_on_conflict,
            "deduplicate": self.deduplicate,
        }