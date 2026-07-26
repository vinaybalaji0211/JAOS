"""Context budget enforcement for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jaos.intelligence.context.context_policy import ContextPolicy
from jaos.intelligence.context.context_token_estimator import (
    ContextTokenEstimator,
)
from jaos.intelligence.exceptions import IntelligenceContextError
from jaos.intelligence.models import (
    ContextItem,
    IntelligenceContextType,
)


def _is_protected_context(item: ContextItem) -> bool:
    """Return whether an item is protected from truncation."""

    required_context = item.metadata.get("required_context", False)
    security_constraint = item.metadata.get(
        "security_constraint",
        False,
    )

    if not isinstance(required_context, bool):
        raise TypeError(
            "context item metadata required_context must be boolean"
        )

    if not isinstance(security_constraint, bool):
        raise TypeError(
            "context item metadata security_constraint must be boolean"
        )

    return (
        item.context_type is IntelligenceContextType.PERMISSION
        or required_context
        or security_constraint
    )


@dataclass(frozen=True, slots=True)
class ContextBudgetResult:
    """Result produced by context token-budget enforcement."""

    selected_items: tuple[ContextItem, ...] = ()
    excluded_item_ids: tuple[str, ...] = ()
    total_estimated_tokens: int = 0
    truncated: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.selected_items, (tuple, list)):
            raise TypeError("selected_items must be a tuple or list")

        if not all(
            isinstance(item, ContextItem)
            for item in self.selected_items
        ):
            raise TypeError(
                "selected_items must contain ContextItem instances"
            )

        if not isinstance(self.excluded_item_ids, (tuple, list)):
            raise TypeError(
                "excluded_item_ids must be a tuple or list"
            )

        if (
            isinstance(self.total_estimated_tokens, bool)
            or not isinstance(self.total_estimated_tokens, int)
        ):
            raise TypeError(
                "total_estimated_tokens must be an integer"
            )

        if self.total_estimated_tokens < 0:
            raise ValueError(
                "total_estimated_tokens must not be negative"
            )

        if not isinstance(self.truncated, bool):
            raise TypeError("truncated must be a boolean")

        object.__setattr__(
            self,
            "selected_items",
            tuple(self.selected_items),
        )
        object.__setattr__(
            self,
            "excluded_item_ids",
            tuple(dict.fromkeys(self.excluded_item_ids)),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe budget result."""

        return {
            "selected_item_ids": [
                item.item_id for item in self.selected_items
            ],
            "excluded_item_ids": list(self.excluded_item_ids),
            "total_estimated_tokens": self.total_estimated_tokens,
            "truncated": self.truncated,
        }


class ContextBudgetManager:
    """Selects ranked context within configured limits."""

    def __init__(
        self,
        token_estimator: ContextTokenEstimator | None = None,
    ) -> None:
        if (
            token_estimator is not None
            and not isinstance(token_estimator, ContextTokenEstimator)
        ):
            raise TypeError(
                "token_estimator must be a ContextTokenEstimator or None"
            )

        self._token_estimator = (
            token_estimator or ContextTokenEstimator()
        )

    def select_items(
        self,
        ranked_items: tuple[ContextItem, ...],
        policy: ContextPolicy,
    ) -> ContextBudgetResult:
        """Select ranked items while preserving protected context."""

        if not isinstance(ranked_items, (tuple, list)):
            raise TypeError("ranked_items must be a tuple or list")

        if not isinstance(policy, ContextPolicy):
            raise TypeError("policy must be an instance of ContextPolicy")

        normalized_items = tuple(ranked_items)

        if not all(
            isinstance(item, ContextItem)
            for item in normalized_items
        ):
            raise TypeError(
                "ranked_items must contain ContextItem instances"
            )

        estimated_items = tuple(
            self._token_estimator.apply_estimate(item)
            for item in normalized_items
        )
        protected_items = tuple(
            item
            for item in estimated_items
            if _is_protected_context(item)
        )
        protected_tokens = sum(
            item.estimated_tokens for item in protected_items
        )

        if len(protected_items) > policy.max_items:
            raise IntelligenceContextError(
                "protected context exceeds the context item limit",
                details={
                    "protected_item_ids": [
                        item.item_id for item in protected_items
                    ],
                    "protected_item_count": len(protected_items),
                    "max_items": policy.max_items,
                },
            )

        if protected_tokens > policy.max_tokens:
            raise IntelligenceContextError(
                "protected context exceeds the token budget",
                details={
                    "protected_item_ids": [
                        item.item_id for item in protected_items
                    ],
                    "protected_tokens": protected_tokens,
                    "max_tokens": policy.max_tokens,
                },
            )

        selected_item_ids = {
            item.item_id for item in protected_items
        }
        total_estimated_tokens = protected_tokens

        for item in estimated_items:
            if item.item_id in selected_item_ids:
                continue

            exceeds_item_limit = (
                len(selected_item_ids) >= policy.max_items
            )
            exceeds_token_limit = (
                total_estimated_tokens + item.estimated_tokens
                > policy.max_tokens
            )

            if exceeds_item_limit or exceeds_token_limit:
                continue

            selected_item_ids.add(item.item_id)
            total_estimated_tokens += item.estimated_tokens

        selected_items = tuple(
            item
            for item in estimated_items
            if item.item_id in selected_item_ids
        )
        excluded_item_ids = tuple(
            item.item_id
            for item in estimated_items
            if item.item_id not in selected_item_ids
        )

        return ContextBudgetResult(
            selected_items=selected_items,
            excluded_item_ids=excluded_item_ids,
            total_estimated_tokens=total_estimated_tokens,
            truncated=bool(excluded_item_ids),
        )