"""Context manager implementation for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock

from jaos.intelligence.context.context_budget_manager import (
    ContextBudgetManager,
)
from jaos.intelligence.context.context_conflict_detector import (
    ContextConflictDetector,
)
from jaos.intelligence.context.context_deduplicator import (
    ContextDeduplicator,
)
from jaos.intelligence.context.context_filter import ContextFilter
from jaos.intelligence.context.context_policy import ContextPolicy
from jaos.intelligence.context.context_policy_registry import (
    ContextPolicyRegistry,
)
from jaos.intelligence.context.context_ranker import ContextRanker
from jaos.intelligence.context.context_source_registry import (
    ContextSourceRegistry,
)
from jaos.intelligence.exceptions import (
    IntelligenceComponentStateError,
    IntelligenceContextError,
)
from jaos.intelligence.interfaces import (
    IntelligenceContextManager,
    IntelligenceContextSource,
)
from jaos.intelligence.models import (
    ContextBundle,
    ContextItem,
    IntelligenceRequest,
    IntelligenceScope,
)


class DefaultIntelligenceContextManager(IntelligenceContextManager):
    """Default provider-independent intelligence context manager."""

    def __init__(
        self,
        *,
        source_registry: ContextSourceRegistry | None = None,
        policy_registry: ContextPolicyRegistry | None = None,
        context_filter: ContextFilter | None = None,
        context_ranker: ContextRanker | None = None,
        context_deduplicator: ContextDeduplicator | None = None,
        conflict_detector: ContextConflictDetector | None = None,
        budget_manager: ContextBudgetManager | None = None,
    ) -> None:
        if (
            source_registry is not None
            and not isinstance(source_registry, ContextSourceRegistry)
        ):
            raise TypeError(
                "source_registry must be a ContextSourceRegistry or None"
            )

        if (
            policy_registry is not None
            and not isinstance(policy_registry, ContextPolicyRegistry)
        ):
            raise TypeError(
                "policy_registry must be a ContextPolicyRegistry or None"
            )

        if (
            context_filter is not None
            and not isinstance(context_filter, ContextFilter)
        ):
            raise TypeError(
                "context_filter must be a ContextFilter or None"
            )

        if (
            context_ranker is not None
            and not isinstance(context_ranker, ContextRanker)
        ):
            raise TypeError(
                "context_ranker must be a ContextRanker or None"
            )

        if (
            context_deduplicator is not None
            and not isinstance(
                context_deduplicator,
                ContextDeduplicator,
            )
        ):
            raise TypeError(
                "context_deduplicator must be a "
                "ContextDeduplicator or None"
            )

        if (
            conflict_detector is not None
            and not isinstance(
                conflict_detector,
                ContextConflictDetector,
            )
        ):
            raise TypeError(
                "conflict_detector must be a "
                "ContextConflictDetector or None"
            )

        if (
            budget_manager is not None
            and not isinstance(budget_manager, ContextBudgetManager)
        ):
            raise TypeError(
                "budget_manager must be a ContextBudgetManager or None"
            )

        self._source_registry = (
            source_registry or ContextSourceRegistry()
        )
        self._policy_registry = (
            policy_registry or ContextPolicyRegistry()
        )
        self._context_filter = context_filter or ContextFilter()
        self._context_ranker = context_ranker or ContextRanker()
        self._context_deduplicator = (
            context_deduplicator or ContextDeduplicator()
        )
        self._conflict_detector = (
            conflict_detector or ContextConflictDetector()
        )
        self._budget_manager = (
            budget_manager or ContextBudgetManager()
        )
        self._ready = False
        self._lock = RLock()

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return "intelligence-context-manager"

    @property
    def is_ready(self) -> bool:
        """Return whether the manager can assemble context."""

        with self._lock:
            return self._ready

    @property
    def source_registry(self) -> ContextSourceRegistry:
        """Return the context source registry."""

        return self._source_registry

    @property
    def policy_registry(self) -> ContextPolicyRegistry:
        """Return the named context policy registry."""

        return self._policy_registry

    def initialize(self) -> None:
        """Mark the context manager ready for context assembly."""

        with self._lock:
            self._ready = True

    def shutdown(self) -> None:
        """Stop accepting context assembly operations."""

        with self._lock:
            self._ready = False

    def register_source(
        self,
        source: IntelligenceContextSource,
    ) -> None:
        """Register a provider-independent context source."""

        self._source_registry.register_source(source)

    def unregister_source(
        self,
        source_name: str,
    ) -> IntelligenceContextSource:
        """Unregister and return a context source."""

        return self._source_registry.unregister_source(source_name)

    def register_policy(
        self,
        policy_name: str,
        policy: ContextPolicy,
        *,
        replace: bool = False,
    ) -> None:
        """Register a named context policy."""

        self._policy_registry.register_policy(
            policy_name,
            policy,
            replace=replace,
        )

    def unregister_policy(
        self,
        policy_name: str,
    ) -> ContextPolicy:
        """Unregister and return a named context policy."""

        return self._policy_registry.unregister_policy(policy_name)

    def assemble_context(
        self,
        request: IntelligenceRequest,
        candidate_items: tuple[ContextItem, ...] = (),
    ) -> ContextBundle:
        """Assemble a validated context bundle."""

        if not self.is_ready:
            raise IntelligenceComponentStateError(
                "intelligence context manager is not ready",
                request_id=getattr(request, "request_id", None),
                component=self.component_name,
            )

        if not isinstance(request, IntelligenceRequest):
            raise TypeError(
                "request must be an instance of IntelligenceRequest"
            )

        if not isinstance(candidate_items, (tuple, list)):
            raise TypeError(
                "candidate_items must be a tuple or list"
            )

        if not all(
            isinstance(item, ContextItem)
            for item in candidate_items
        ):
            raise TypeError(
                "candidate_items must contain ContextItem instances"
            )

        policy = self._policy_registry.resolve(
            request.context_policy
        )
        resolved_policy_name = (
            request.context_policy.strip().lower()
            if request.context_policy is not None
            else ContextPolicyRegistry.DEFAULT_POLICY_NAME
        )
        collected_items = list(candidate_items)
        source_errors: dict[str, str] = {}

        for source in self._source_registry.list_sources():
            source_name = source.source_name.strip().lower()

            if not source.is_ready:
                message = "context source is not ready"
                source_errors[source_name] = message

                if policy.fail_on_source_error:
                    raise IntelligenceContextError(
                        message,
                        request_id=request.request_id,
                        details={"source_name": source_name},
                    )

                continue

            try:
                source_items = source.collect_context(request)

                if not isinstance(source_items, (tuple, list)):
                    raise TypeError(
                        "context source must return a tuple or list"
                    )

                if not all(
                    isinstance(item, ContextItem)
                    for item in source_items
                ):
                    raise TypeError(
                        "context source returned an invalid item"
                    )

                collected_items.extend(source_items)
            except Exception as exc:
                source_errors[source_name] = str(exc)

                if policy.fail_on_source_error:
                    raise IntelligenceContextError(
                        f"context source failed: {source_name}",
                        request_id=request.request_id,
                        details={
                            "source_name": source_name,
                            "error": str(exc),
                        },
                    ) from exc

        filter_result = self._context_filter.filter_items(
            request=request,
            items=tuple(collected_items),
            policy=policy,
        )
        ranking_result = self._context_ranker.rank_items(
            filter_result.included_items
        )

        if policy.deduplicate:
            deduplication_result = (
                self._context_deduplicator.deduplicate(
                    ranking_result.ranked_items
                )
            )
            ranked_items = deduplication_result.retained_items
            duplicate_item_ids = (
                deduplication_result.duplicate_item_ids
            )
            duplicate_of = deduplication_result.duplicate_of
        else:
            ranked_items = ranking_result.ranked_items
            duplicate_item_ids = ()
            duplicate_of = {}

        conflict_result = self._conflict_detector.detect_conflicts(
            ranked_items
        )

        if conflict_result.has_conflicts and policy.fail_on_conflict:
            raise IntelligenceContextError(
                "conflicting context items detected",
                request_id=request.request_id,
                details=conflict_result.to_dict(),
            )

        budget_result = self._budget_manager.select_items(
            ranked_items,
            policy,
        )
        selected_item_ids = {
            item.item_id for item in budget_result.selected_items
        }

        excluded_item_ids = tuple(
            dict.fromkeys(
                (
                    *filter_result.excluded_item_ids,
                    *duplicate_item_ids,
                    *budget_result.excluded_item_ids,
                )
            )
        )
        selected_conflict_ids = tuple(
            item_id
            for item_id in conflict_result.conflict_item_ids
            if item_id in selected_item_ids
        )

        bundle = ContextBundle(
            request_id=request.request_id,
            identity=request.identity,
            items=budget_result.selected_items,
            max_tokens=policy.max_tokens,
            context_policy=resolved_policy_name,
            excluded_item_ids=excluded_item_ids,
            conflict_item_ids=selected_conflict_ids,
            truncated=budget_result.truncated,
            metadata={
                "resolved_policy_name": resolved_policy_name,
                "resolved_policy": policy.to_dict(),
                "candidate_item_count": len(collected_items),
                "selected_item_count": len(
                    budget_result.selected_items
                ),
                "registered_source_count": len(
                    self._source_registry
                ),
                "source_errors": source_errors,
                "filter": filter_result.to_dict(),
                "ranking": ranking_result.to_dict(),
                "deduplication": {
                    "duplicate_item_ids": list(
                        duplicate_item_ids
                    ),
                    "duplicate_of": dict(duplicate_of),
                },
                "conflicts": conflict_result.to_dict(),
                "budget": budget_result.to_dict(),
                "assembled_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            },
        )

        self.validate_context(bundle)

        return bundle

    def validate_context(self, bundle: ContextBundle) -> None:
        """Validate an assembled context bundle."""

        if not isinstance(bundle, ContextBundle):
            raise TypeError(
                "bundle must be an instance of ContextBundle"
            )

        policy = (
            self._policy_registry.resolve(bundle.context_policy)
            if bundle.context_policy is not None
            else None
        )
        current_time = datetime.now(timezone.utc)
        validation_errors: list[str] = []

        if (
            bundle.max_tokens is not None
            and bundle.total_estimated_tokens > bundle.max_tokens
        ):
            validation_errors.append("bundle exceeds its token budget")

        if policy is not None:
            if bundle.max_tokens != policy.max_tokens:
                validation_errors.append(
                    "bundle max_tokens does not match context policy"
                )

            if len(bundle.items) > policy.max_items:
                validation_errors.append(
                    "bundle exceeds context policy item limit"
                )

        for item in bundle.items:
            if (
                item.identity.scope is not IntelligenceScope.GLOBAL
                and item.identity != bundle.identity
            ):
                validation_errors.append(
                    f"identity mismatch for item: {item.item_id}"
                )

            if policy is None:
                continue

            if item.context_type not in policy.allowed_context_types:
                validation_errors.append(
                    f"context type not allowed: {item.item_id}"
                )

            if item.trust_level not in policy.allowed_trust_levels:
                validation_errors.append(
                    f"trust level not allowed: {item.item_id}"
                )

            if item.relevance < policy.minimum_relevance:
                validation_errors.append(
                    f"relevance below policy minimum: {item.item_id}"
                )

            if item.importance < policy.minimum_importance:
                validation_errors.append(
                    f"importance below policy minimum: {item.item_id}"
                )

            if (
                not policy.include_expired
                and item.expires_at is not None
                and item.expires_at <= current_time
            ):
                validation_errors.append(
                    f"expired context item: {item.item_id}"
                )

        if validation_errors:
            raise IntelligenceContextError(
                "context bundle validation failed",
                request_id=bundle.request_id,
                details={"validation_errors": validation_errors},
            )