"""Context ranking for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jaos.intelligence.models import ContextItem, ContextTrustLevel


TRUST_SCORES: dict[ContextTrustLevel, float] = {
    ContextTrustLevel.TRUSTED_SYSTEM: 1.0,
    ContextTrustLevel.TRUSTED_INTERNAL: 0.9,
    ContextTrustLevel.USER_PROVIDED: 0.75,
    ContextTrustLevel.RETRIEVED_MEMORY: 0.65,
    ContextTrustLevel.EXTERNAL_UNTRUSTED: 0.2,
}


def _validate_weight(value: float, field_name: str) -> float:
    """Validate a non-negative ranking weight."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")

    normalized = float(value)

    if normalized < 0.0:
        raise ValueError(f"{field_name} must not be negative")

    return normalized


@dataclass(frozen=True, slots=True)
class ContextRankingResult:
    """Result produced by deterministic context ranking."""

    ranked_items: tuple[ContextItem, ...] = ()
    scores: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.ranked_items, (tuple, list)):
            raise TypeError("ranked_items must be a tuple or list")

        if not all(
            isinstance(item, ContextItem)
            for item in self.ranked_items
        ):
            raise TypeError(
                "ranked_items must contain ContextItem instances"
            )

        if not isinstance(self.scores, dict):
            raise TypeError("scores must be a dictionary")

        object.__setattr__(
            self,
            "ranked_items",
            tuple(self.ranked_items),
        )
        object.__setattr__(self, "scores", dict(self.scores))

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe ranking result."""

        return {
            "ranked_item_ids": [
                item.item_id for item in self.ranked_items
            ],
            "scores": dict(self.scores),
        }


class ContextRanker:
    """Ranks context items using normalized deterministic weights."""

    def __init__(
        self,
        *,
        relevance_weight: float = 0.45,
        importance_weight: float = 0.25,
        confidence_weight: float = 0.20,
        trust_weight: float = 0.10,
    ) -> None:
        weights = {
            "relevance_weight": _validate_weight(
                relevance_weight,
                "relevance_weight",
            ),
            "importance_weight": _validate_weight(
                importance_weight,
                "importance_weight",
            ),
            "confidence_weight": _validate_weight(
                confidence_weight,
                "confidence_weight",
            ),
            "trust_weight": _validate_weight(
                trust_weight,
                "trust_weight",
            ),
        }
        total_weight = sum(weights.values())

        if total_weight <= 0.0:
            raise ValueError(
                "at least one context ranking weight must be positive"
            )

        self._relevance_weight = (
            weights["relevance_weight"] / total_weight
        )
        self._importance_weight = (
            weights["importance_weight"] / total_weight
        )
        self._confidence_weight = (
            weights["confidence_weight"] / total_weight
        )
        self._trust_weight = weights["trust_weight"] / total_weight

    def score_item(self, item: ContextItem) -> float:
        """Return the normalized ranking score for one context item."""

        if not isinstance(item, ContextItem):
            raise TypeError("item must be an instance of ContextItem")

        trust_score = TRUST_SCORES[item.trust_level]

        return (
            item.relevance * self._relevance_weight
            + item.importance * self._importance_weight
            + item.confidence * self._confidence_weight
            + trust_score * self._trust_weight
        )

    def rank_items(
        self,
        items: tuple[ContextItem, ...],
    ) -> ContextRankingResult:
        """Rank context items from highest to lowest value."""

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

        scores = {
            item.item_id: self.score_item(item)
            for item in normalized_items
        }

        ranked_items = tuple(
            sorted(
                normalized_items,
                key=lambda item: (
                    -scores[item.item_id],
                    -TRUST_SCORES[item.trust_level],
                    -item.importance,
                    -item.relevance,
                    -item.created_at.timestamp(),
                    item.item_id,
                ),
            )
        )

        return ContextRankingResult(
            ranked_items=ranked_items,
            scores=scores,
        )