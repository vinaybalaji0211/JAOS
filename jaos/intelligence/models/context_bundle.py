"""Context bundle model for the JAOS AI Intelligence Platform."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from jaos.intelligence.models.context_item import ContextItem
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""

    return datetime.now(timezone.utc)


def _normalize_identifier_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> tuple[str, ...]:
    """Normalize and deduplicate a tuple of identifiers."""

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

        if value not in normalized:
            normalized.append(value)

    return tuple(normalized)


@dataclass(frozen=True, slots=True)
class ContextBundle:
    """Represents the validated context assembled for one request."""

    request_id: str
    identity: IntelligenceIdentity
    items: tuple[ContextItem, ...] = ()
    bundle_id: str = field(default_factory=lambda: str(uuid4()))
    max_tokens: int | None = None
    context_policy: str | None = None
    excluded_item_ids: tuple[str, ...] = ()
    conflict_item_ids: tuple[str, ...] = ()
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_utc_now)
    total_estimated_tokens: int = field(init=False)

    def __post_init__(self) -> None:
        """Validate and normalize context bundle invariants."""

        required_strings = {
            "bundle_id": self.bundle_id,
            "request_id": self.request_id,
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
            items = tuple(self.items)
        except TypeError as exc:
            raise TypeError(
                "items must be a collection of ContextItem instances"
            ) from exc

        for item in items:
            if not isinstance(item, ContextItem):
                raise TypeError(
                    "items must contain only ContextItem instances"
                )

        item_ids = tuple(item.item_id for item in items)

        if len(item_ids) != len(set(item_ids)):
            raise ValueError("context item IDs must be unique")

        if self.max_tokens is not None:
            if isinstance(self.max_tokens, bool) or not isinstance(
                self.max_tokens,
                int,
            ):
                raise TypeError("max_tokens must be an integer or None")

            if self.max_tokens <= 0:
                raise ValueError(
                    "max_tokens must be greater than zero"
                )

        if self.context_policy is not None and not isinstance(
            self.context_policy,
            str,
        ):
            raise TypeError("context_policy must be a string or None")

        if not isinstance(self.truncated, bool):
            raise TypeError("truncated must be a boolean")

        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

        if not isinstance(self.created_at, datetime):
            raise TypeError("created_at must be a datetime instance")

        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")

        excluded_item_ids = _normalize_identifier_tuple(
            self.excluded_item_ids,
            "excluded_item_ids",
        )
        conflict_item_ids = _normalize_identifier_tuple(
            self.conflict_item_ids,
            "conflict_item_ids",
        )

        included_ids = set(item_ids)

        if included_ids.intersection(excluded_item_ids):
            raise ValueError(
                "excluded_item_ids must not reference included items"
            )

        if not set(conflict_item_ids).issubset(included_ids):
            raise ValueError(
                "conflict_item_ids must reference included items"
            )

        total_estimated_tokens = sum(
            item.estimated_tokens
            for item in items
        )

        if (
            self.max_tokens is not None
            and total_estimated_tokens > self.max_tokens
        ):
            raise ValueError(
                "context items exceed max_tokens"
            )

        context_policy = (
            self.context_policy.strip().lower()
            if self.context_policy is not None
            else None
        )

        object.__setattr__(self, "bundle_id", self.bundle_id.strip())
        object.__setattr__(self, "request_id", self.request_id.strip())
        object.__setattr__(self, "items", items)
        object.__setattr__(
            self,
            "context_policy",
            context_policy or None,
        )
        object.__setattr__(
            self,
            "excluded_item_ids",
            excluded_item_ids,
        )
        object.__setattr__(
            self,
            "conflict_item_ids",
            conflict_item_ids,
        )
        object.__setattr__(self, "metadata", dict(self.metadata))
        object.__setattr__(
            self,
            "total_estimated_tokens",
            total_estimated_tokens,
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a platform-independent dictionary representation."""

        return {
            "bundle_id": self.bundle_id,
            "request_id": self.request_id,
            "identity": self.identity.to_dict(),
            "items": [item.to_dict() for item in self.items],
            "total_estimated_tokens": self.total_estimated_tokens,
            "max_tokens": self.max_tokens,
            "context_policy": self.context_policy,
            "excluded_item_ids": list(self.excluded_item_ids),
            "conflict_item_ids": list(self.conflict_item_ids),
            "truncated": self.truncated,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
        }