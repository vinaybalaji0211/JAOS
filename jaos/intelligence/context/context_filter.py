"""Context filtering for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from jaos.intelligence.context.context_policy import ContextPolicy
from jaos.intelligence.exceptions import IntelligenceContextError
from jaos.intelligence.models import (
    ContextItem,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceScope,
)


def _normalize_now(value: datetime | None) -> datetime:
    """Return an aware UTC timestamp."""

    if value is None:
        return datetime.now(timezone.utc)

    if not isinstance(value, datetime):
        raise TypeError("now must be a datetime or None")

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("now must be timezone-aware")

    return value.astimezone(timezone.utc)


def _identity_can_access(
    request_identity: IntelligenceIdentity,
    item_identity: IntelligenceIdentity,
) -> bool:
    """Return whether a request identity may access an item identity."""

    if item_identity.scope is IntelligenceScope.GLOBAL:
        return True

    return item_identity == request_identity


@dataclass(frozen=True, slots=True)
class ContextFilterResult:
    """Result produced by context filtering."""

    included_items: tuple[ContextItem, ...] = ()
    excluded_item_ids: tuple[str, ...] = ()
    exclusion_reasons: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.included_items, (tuple, list)):
            raise TypeError("included_items must be a tuple or list")

        if not all(
            isinstance(item, ContextItem)
            for item in self.included_items
        ):
            raise TypeError(
                "included_items must contain ContextItem instances"
            )

        if not isinstance(self.excluded_item_ids, (tuple, list)):
            raise TypeError("excluded_item_ids must be a tuple or list")

        normalized_excluded_ids: list[str] = []

        for item_id in self.excluded_item_ids:
            if not isinstance(item_id, str) or not item_id.strip():
                raise ValueError(
                    "excluded_item_ids must contain non-empty strings"
                )

            normalized = item_id.strip()

            if normalized not in normalized_excluded_ids:
                normalized_excluded_ids.append(normalized)

        if not isinstance(self.exclusion_reasons, dict):
            raise TypeError("exclusion_reasons must be a dictionary")

        object.__setattr__(
            self,
            "included_items",
            tuple(self.included_items),
        )
        object.__setattr__(
            self,
            "excluded_item_ids",
            tuple(normalized_excluded_ids),
        )
        object.__setattr__(
            self,
            "exclusion_reasons",
            dict(self.exclusion_reasons),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return a serialization-safe filtering result."""

        return {
            "included_item_ids": [
                item.item_id for item in self.included_items
            ],
            "excluded_item_ids": list(self.excluded_item_ids),
            "exclusion_reasons": dict(self.exclusion_reasons),
        }


class ContextFilter:
    """Applies context visibility and policy rules."""

    def filter_items(
        self,
        request: IntelligenceRequest,
        items: tuple[ContextItem, ...],
        policy: ContextPolicy,
        *,
        now: datetime | None = None,
    ) -> ContextFilterResult:
        """Filter candidate context items for a request."""

        if not isinstance(request, IntelligenceRequest):
            raise TypeError(
                "request must be an instance of IntelligenceRequest"
            )

        if not isinstance(items, (tuple, list)):
            raise TypeError("items must be a tuple or list")

        if not isinstance(policy, ContextPolicy):
            raise TypeError("policy must be an instance of ContextPolicy")

        current_time = _normalize_now(now)
        included_items: list[ContextItem] = []
        excluded_item_ids: list[str] = []
        exclusion_reasons: dict[str, str] = {}
        encountered_item_ids: set[str] = set()

        for item in items:
            if not isinstance(item, ContextItem):
                raise TypeError(
                    "items must contain ContextItem instances"
                )

            if item.item_id in encountered_item_ids:
                raise IntelligenceContextError(
                    f"duplicate context item ID: {item.item_id}",
                    request_id=request.request_id,
                    details={"item_id": item.item_id},
                )

            encountered_item_ids.add(item.item_id)

            exclusion_reason = self._get_exclusion_reason(
                request=request,
                item=item,
                policy=policy,
                current_time=current_time,
            )

            if exclusion_reason is None:
                included_items.append(item)
                continue

            excluded_item_ids.append(item.item_id)
            exclusion_reasons[item.item_id] = exclusion_reason

        return ContextFilterResult(
            included_items=tuple(included_items),
            excluded_item_ids=tuple(excluded_item_ids),
            exclusion_reasons=exclusion_reasons,
        )

    @staticmethod
    def _get_exclusion_reason(
        *,
        request: IntelligenceRequest,
        item: ContextItem,
        policy: ContextPolicy,
        current_time: datetime,
    ) -> str | None:
        """Return the first policy reason that excludes an item."""

        if item.context_type not in policy.allowed_context_types:
            return "context_type_not_allowed"

        if item.trust_level not in policy.allowed_trust_levels:
            return "trust_level_not_allowed"

        if item.relevance < policy.minimum_relevance:
            return "below_minimum_relevance"

        if item.importance < policy.minimum_importance:
            return "below_minimum_importance"

        if (
            not policy.include_expired
            and item.expires_at is not None
            and item.expires_at <= current_time
        ):
            return "expired"

        if not _identity_can_access(request.identity, item.identity):
            return "identity_scope_mismatch"

        required_permissions = set(item.permission_constraints)
        request_permissions = set(request.permission_constraints)

        if not required_permissions.issubset(request_permissions):
            return "permission_scope_mismatch"

        return None