"""Memory Platform context source for JAOS Intelligence."""

from __future__ import annotations

from threading import RLock
from typing import Any

from jaos.intelligence.exceptions import (
    IntelligenceComponentStateError,
    IntelligenceContextError,
)
from jaos.intelligence.interfaces import IntelligenceContextSource
from jaos.intelligence.models import (
    ContextItem,
    ContextTrustLevel,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceScope,
)
from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_lifecycle_state import (
    MemoryLifecycleState,
)
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.storage.memory_search_engine import MemorySearchEngine


INTELLIGENCE_TO_MEMORY_SCOPE: dict[
    IntelligenceScope,
    MemoryScope,
] = {
    IntelligenceScope.GLOBAL: MemoryScope.GLOBAL,
    IntelligenceScope.SYSTEM: MemoryScope.SYSTEM,
    IntelligenceScope.USER: MemoryScope.USER,
    IntelligenceScope.SESSION: MemoryScope.SESSION,
    IntelligenceScope.MISSION: MemoryScope.MISSION,
}

MEMORY_TO_INTELLIGENCE_SCOPE: dict[
    MemoryScope,
    IntelligenceScope,
] = {
    memory_scope: intelligence_scope
    for intelligence_scope, memory_scope
    in INTELLIGENCE_TO_MEMORY_SCOPE.items()
}


def _normalize_source_name(source_name: str) -> str:
    """Validate and normalize a source name."""

    if not isinstance(source_name, str):
        raise TypeError("source_name must be a string")

    normalized = source_name.strip().lower()

    if not normalized:
        raise ValueError("source_name must not be empty")

    return normalized


def _validate_score(value: float, field_name: str) -> float:
    """Validate a score between zero and one."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field_name} must be numeric")

    normalized = float(value)

    if not 0.0 <= normalized <= 1.0:
        raise ValueError(f"{field_name} must be between 0.0 and 1.0")

    return normalized


def _to_memory_identity(
    identity: IntelligenceIdentity,
) -> MemoryIdentity:
    """Convert an Intelligence identity into a Memory identity."""

    memory_scope = INTELLIGENCE_TO_MEMORY_SCOPE.get(identity.scope)

    if memory_scope is None:
        raise IntelligenceContextError(
            "intelligence identity scope is not supported by "
            "the Memory Platform",
            details={"scope": identity.scope.value},
        )

    return MemoryIdentity(
        scope=memory_scope,
        identity_id=identity.identity_id,
    )


def _to_intelligence_identity(
    identity: MemoryIdentity,
) -> IntelligenceIdentity:
    """Convert a Memory identity into an Intelligence identity."""

    intelligence_scope = MEMORY_TO_INTELLIGENCE_SCOPE.get(
        identity.scope
    )

    if intelligence_scope is None:
        raise IntelligenceContextError(
            "memory identity scope is not supported by "
            "the Intelligence Platform",
            details={"scope": identity.scope.value},
        )

    return IntelligenceIdentity(
        scope=intelligence_scope,
        identity_id=identity.identity_id,
    )


def _normalize_permissions(
    value: Any,
) -> tuple[str, ...]:
    """Normalize permission constraints from memory metadata."""

    if value is None:
        return ()

    if not isinstance(value, (tuple, list)):
        raise TypeError(
            "memory metadata permission_constraints must be "
            "a tuple or list"
        )

    normalized_permissions: list[str] = []

    for permission in value:
        if not isinstance(permission, str):
            raise TypeError(
                "memory permission constraints must be strings"
            )

        normalized = permission.strip().lower()

        if not normalized:
            raise ValueError(
                "memory permission constraints must not be empty"
            )

        if normalized not in normalized_permissions:
            normalized_permissions.append(normalized)

    return tuple(normalized_permissions)


def _estimated_tokens(record: MemoryRecord) -> int:
    """Return an optional stored token estimate."""

    value = record.metadata.get("estimated_tokens", 0)

    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            "memory metadata estimated_tokens must be an integer"
        )

    if value < 0:
        raise ValueError(
            "memory metadata estimated_tokens must not be negative"
        )

    return value


def _relevance_score(
    record: MemoryRecord,
    *,
    result_index: int,
    result_count: int,
) -> float:
    """Return stored relevance or deterministic result-rank relevance."""

    stored_relevance = record.metadata.get("relevance")

    if stored_relevance is not None:
        return _validate_score(
            stored_relevance,
            "memory relevance",
        )

    if result_count <= 1:
        return 1.0

    return 1.0 - (0.4 * (result_index / (result_count - 1)))


class MemoryContextSource(IntelligenceContextSource):
    """Adapts Memory Platform search results into context items."""

    def __init__(
        self,
        search_engine: MemorySearchEngine,
        *,
        source_name: str = "memory-platform",
        memory_types: tuple[MemoryType, ...] = (),
        minimum_importance: float = 0.0,
        minimum_confidence: float = 0.0,
        max_results: int = 10,
        include_archived: bool = False,
    ) -> None:
        if not isinstance(search_engine, MemorySearchEngine):
            raise TypeError(
                "search_engine must implement MemorySearchEngine"
            )

        if not isinstance(memory_types, tuple):
            raise TypeError("memory_types must be a tuple")

        if not all(
            isinstance(memory_type, MemoryType)
            for memory_type in memory_types
        ):
            raise TypeError(
                "memory_types must contain MemoryType instances"
            )

        if isinstance(max_results, bool) or not isinstance(
            max_results,
            int,
        ):
            raise TypeError("max_results must be an integer")

        if max_results <= 0:
            raise ValueError("max_results must be greater than zero")

        if not isinstance(include_archived, bool):
            raise TypeError("include_archived must be a boolean")

        self._search_engine = search_engine
        self._source_name = _normalize_source_name(source_name)
        self._memory_types = memory_types
        self._minimum_importance = _validate_score(
            minimum_importance,
            "minimum_importance",
        )
        self._minimum_confidence = _validate_score(
            minimum_confidence,
            "minimum_confidence",
        )
        self._max_results = max_results
        self._include_archived = include_archived
        self._ready = False
        self._lock = RLock()

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return f"context-source:{self._source_name}"

    @property
    def source_name(self) -> str:
        """Return the stable context-source name."""

        return self._source_name

    @property
    def is_ready(self) -> bool:
        """Return whether memory context can be collected."""

        with self._lock:
            return self._ready

    def initialize(self) -> None:
        """Enable Memory Platform retrieval."""

        with self._lock:
            self._ready = True

    def shutdown(self) -> None:
        """Disable Memory Platform retrieval."""

        with self._lock:
            self._ready = False

    def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        """Retrieve and adapt approved memories for a request."""

        if not isinstance(request, IntelligenceRequest):
            raise TypeError(
                "request must be an instance of IntelligenceRequest"
            )

        if not self.is_ready:
            raise IntelligenceComponentStateError(
                "memory context source is not ready",
                request_id=request.request_id,
                component=self.component_name,
            )

        memory_identity = _to_memory_identity(request.identity)
        memory_query = MemoryQuery(
            query_text=request.objective,
            memory_types=self._memory_types,
            scope=memory_identity.scope,
            identity=memory_identity,
            minimum_importance=self._minimum_importance,
            minimum_confidence=self._minimum_confidence,
            max_results=self._max_results,
        )

        try:
            result = self._search_engine.search(memory_query)
        except Exception as exc:
            raise IntelligenceContextError(
                "Memory Platform retrieval failed",
                request_id=request.request_id,
                details={"error": str(exc)},
            ) from exc

        if not isinstance(result, MemoryResult):
            raise IntelligenceContextError(
                "Memory Platform returned an invalid result",
                request_id=request.request_id,
            )

        records = tuple(result.records)
        context_items: list[ContextItem] = []

        for index, record in enumerate(records):
            if not isinstance(record, MemoryRecord):
                raise IntelligenceContextError(
                    "Memory Platform returned an invalid record",
                    request_id=request.request_id,
                )

            if record.lifecycle_state in {
                MemoryLifecycleState.EXPIRED,
                MemoryLifecycleState.DELETED,
            }:
                continue

            if (
                record.lifecycle_state
                is MemoryLifecycleState.ARCHIVED
                and not self._include_archived
            ):
                continue

            intelligence_identity = _to_intelligence_identity(
                record.identity
            )

            if (
                intelligence_identity.scope
                is not IntelligenceScope.GLOBAL
                and intelligence_identity != request.identity
            ):
                raise IntelligenceContextError(
                    "Memory Platform returned a record outside "
                    "the request identity scope",
                    request_id=request.request_id,
                    details={"memory_id": record.memory_id},
                )

            memory_metadata = record.metadata.to_dict()
            context_metadata: dict[str, Any] = {
                "memory_id": record.memory_id,
                "memory_type": record.memory_type.value,
                "memory_source": record.source,
                "memory_lifecycle_state": (
                    record.lifecycle_state.value
                ),
                "memory_updated_at": record.updated_at.isoformat(),
                "memory_query_time_ms": result.query_time_ms,
                "memory_total_matches": result.total_matches,
                "memory_metadata": memory_metadata,
            }

            conflict_key = record.metadata.get("conflict_key")

            if conflict_key is not None:
                context_metadata["conflict_key"] = conflict_key

            context_items.append(
                ContextItem(
                    item_id=f"memory:{record.memory_id}",
                    context_type=IntelligenceContextType.MEMORY,
                    content=record.content,
                    identity=intelligence_identity,
                    source=self._source_name,
                    trust_level=(
                        ContextTrustLevel.RETRIEVED_MEMORY
                    ),
                    relevance=_relevance_score(
                        record,
                        result_index=index,
                        result_count=len(records),
                    ),
                    importance=record.importance,
                    confidence=record.confidence,
                    estimated_tokens=_estimated_tokens(record),
                    permission_constraints=_normalize_permissions(
                        record.metadata.get(
                            "permission_constraints",
                            (),
                        )
                    ),
                    metadata=context_metadata,
                    created_at=record.created_at,
                )
            )

        return tuple(context_items)