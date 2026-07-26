"""Context conflict detection for the JAOS AI Intelligence Platform."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from jaos.intelligence.models import ContextItem


def _content_fingerprint(content: Any) -> str:
    """Create a deterministic fingerprint for context content."""

    try:
        return json.dumps(
            content,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
    except (TypeError, ValueError):
        return repr(content)


def _normalize_conflict_key(value: Any) -> str | None:
    """Normalize an optional conflict key."""

    if value is None:
        return None

    if not isinstance(value, str):
        raise TypeError(
            "context item metadata conflict_key must be a string"
        )

    normalized = value.strip().lower()

    if not normalized:
        raise ValueError(
            "context item metadata conflict_key must not be empty"
        )

    return normalized


@dataclass(frozen=True, slots=True)
class ContextConflictResult:
    """Result produced by context conflict detection."""

    conflict_item_ids: tuple[str, ...] = ()
    conflict_groups: dict[str, tuple[str, ...]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if not isinstance(self.conflict_item_ids, (tuple, list)):
            raise TypeError(
                "conflict_item_ids must be a tuple or list"
            )

        if not isinstance(self.conflict_groups, dict):
            raise TypeError("conflict_groups must be a dictionary")

        normalized_ids = tuple(
            dict.fromkeys(self.conflict_item_ids)
        )
        normalized_groups = {
            key: tuple(item_ids)
            for key, item_ids in self.conflict_groups.items()
        }

        object.__setattr__(
            self,
            "conflict_item_ids",
            normalized_ids,
        )
        object.__setattr__(
            self,
            "conflict_groups",
            normalized_groups,
        )

    @property
    def has_conflicts(self) -> bool:
        """Return whether any conflicts were detected."""

        return bool(self.conflict_item_ids)

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe conflict result."""

        return {
            "has_conflicts": self.has_conflicts,
            "conflict_item_ids": list(self.conflict_item_ids),
            "conflict_groups": {
                key: list(item_ids)
                for key, item_ids in self.conflict_groups.items()
            },
        }


class ContextConflictDetector:
    """Detects explicitly keyed contradictory context items."""

    def detect_conflicts(
        self,
        items: tuple[ContextItem, ...],
    ) -> ContextConflictResult:
        """Detect conflicting content among context items."""

        if not isinstance(items, (tuple, list)):
            raise TypeError("items must be a tuple or list")

        normalized_items = tuple(items)

        if not all(
            isinstance(item, ContextItem)
            for item in normalized_items
        ):
            raise TypeError(
                "items must contain ContextItem instances"
            )

        groups: dict[str, list[ContextItem]] = {}

        for item in normalized_items:
            conflict_key = _normalize_conflict_key(
                item.metadata.get("conflict_key")
            )

            if conflict_key is None:
                continue

            groups.setdefault(conflict_key, []).append(item)

        conflict_groups: dict[str, tuple[str, ...]] = {}
        conflict_item_ids: list[str] = []

        for conflict_key, grouped_items in groups.items():
            fingerprints = {
                _content_fingerprint(item.content)
                for item in grouped_items
            }

            if len(fingerprints) <= 1:
                continue

            item_ids = tuple(
                item.item_id for item in grouped_items
            )
            conflict_groups[conflict_key] = item_ids

            for item_id in item_ids:
                if item_id not in conflict_item_ids:
                    conflict_item_ids.append(item_id)

        return ContextConflictResult(
            conflict_item_ids=tuple(conflict_item_ids),
            conflict_groups=conflict_groups,
        )