"""Provider-independent context token estimation for JAOS Intelligence."""

from __future__ import annotations

import json
from dataclasses import replace
from math import ceil
from typing import Any

from jaos.intelligence.models import ContextItem


def _validate_positive_integer(value: int, field_name: str) -> int:
    """Validate a positive integer configuration value."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field_name} must be an integer")

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero")

    return value


def _serialize_content(content: Any) -> str:
    """Convert context content into deterministic estimation text."""

    if isinstance(content, str):
        return content

    try:
        return json.dumps(
            content,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )
    except (TypeError, ValueError):
        return repr(content)


class ContextTokenEstimator:
    """
    Estimates context tokens without depending on an AI provider.

    The default heuristic uses approximately four characters per token
    plus a small per-item structural overhead. Provider-specific token
    counting may replace this implementation through composition later.
    """

    def __init__(
        self,
        *,
        characters_per_token: int = 4,
        item_overhead_tokens: int = 8,
    ) -> None:
        self._characters_per_token = _validate_positive_integer(
            characters_per_token,
            "characters_per_token",
        )
        self._item_overhead_tokens = _validate_positive_integer(
            item_overhead_tokens,
            "item_overhead_tokens",
        )

    def estimate_content(self, content: Any) -> int:
        """Estimate the number of tokens used by arbitrary content."""

        serialized = _serialize_content(content)
        content_tokens = ceil(
            max(len(serialized), 1) / self._characters_per_token
        )

        return content_tokens + self._item_overhead_tokens

    def estimate_item(self, item: ContextItem) -> int:
        """Return an existing source estimate or compute one."""

        if not isinstance(item, ContextItem):
            raise TypeError("item must be an instance of ContextItem")

        if item.estimated_tokens > 0:
            return item.estimated_tokens

        return self.estimate_content(item.content)

    def apply_estimate(self, item: ContextItem) -> ContextItem:
        """Return an item carrying a non-zero token estimate."""

        estimated_tokens = self.estimate_item(item)

        if item.estimated_tokens == estimated_tokens:
            return item

        return replace(item, estimated_tokens=estimated_tokens)