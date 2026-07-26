"""Context deduplication for the JAOS AI Intelligence Platform."""

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


def _deduplication_key(item: ContextItem) -> tuple[str, ...]:
    """Return the semantic deduplication key for an item."""

    return (
        item.context_type.value,
        item.identity.scope.value,
        item.identity.identity_id or "",
        _content_fingerprint(item.content),
    )


@dataclass(frozen=True, slots=True)
class ContextDeduplicationResult:
    """Result produced by semantic context deduplication."""

    retained_items: tuple[ContextItem, ...] = ()
    duplicate_item_ids: tuple[str, ...] = ()
    duplicate_of: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.retained_items, (tuple, list)):
            raise TypeError("retained_items must be a tuple or list")

        if not all(
            isinstance(item, ContextItem)
            for item in self.retained_items
        ):
            raise TypeError(
                "retained_items must contain ContextItem instances"
            )

        if not isinstance(self.duplicate_item_ids, (tuple, list)):
            raise TypeError(
                "duplicate_item_ids must be a tuple or list"
            )

        if not isinstance(self.duplicate_of, dict):
            raise TypeError("duplicate_of must be a dictionary")

        object.__setattr__(
            self,
            "retained_items",
            tuple(self.retained_items),
        )
        object.__setattr__(
            self,
            "duplicate_item_ids",
            tuple(dict.fromkeys(self.duplicate_item_ids)),
        )
        object.__setattr__(
            self,
            "duplicate_of",
            dict(self.duplicate_of),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe deduplication result."""

        return {
            "retained_item_ids": [
                item.item_id for item in self.retained_items
            ],
            "duplicate_item_ids": list(self.duplicate_item_ids),
            "duplicate_of": dict(self.duplicate_of),
        }


class ContextDeduplicator:
    """Removes lower-ranked semantically equivalent context items."""

    def deduplicate(
        self,
        ranked_items: tuple[ContextItem, ...],
    ) -> ContextDeduplicationResult:
        """Retain the first item for every semantic context key."""

        if not isinstance(ranked_items, (tuple, list)):
            raise TypeError("ranked_items must be a tuple or list")

        normalized_items = tuple(ranked_items)

        if not all(
            isinstance(item, ContextItem)
            for item in normalized_items
        ):
            raise TypeError(
                "ranked_items must contain ContextItem instances"
            )

        retained_items: list[ContextItem] = []
        duplicate_item_ids: list[str] = []
        duplicate_of: dict[str, str] = {}
        retained_by_key: dict[tuple[str, ...], ContextItem] = {}

        for item in normalized_items:
            key = _deduplication_key(item)
            retained_item = retained_by_key.get(key)

            if retained_item is None:
                retained_by_key[key] = item
                retained_items.append(item)
                continue

            duplicate_item_ids.append(item.item_id)
            duplicate_of[item.item_id] = retained_item.item_id

        return ContextDeduplicationResult(
            retained_items=tuple(retained_items),
            duplicate_item_ids=tuple(duplicate_item_ids),
            duplicate_of=duplicate_of,
        )