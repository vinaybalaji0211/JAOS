"""Tests for the Memory Platform context source."""

from typing import Any

import pytest

from jaos.intelligence import (
    ContextTrustLevel,
    IntelligenceComponentStateError,
    IntelligenceContextError,
    IntelligenceContextType,
    IntelligenceIdentity,
    IntelligenceRequest,
    IntelligenceRequestType,
    IntelligenceScope,
)
from jaos.intelligence.context import (
    DefaultIntelligenceContextManager,
    MemoryContextSource,
)
from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_lifecycle_state import (
    MemoryLifecycleState,
)
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.storage.memory_search_engine import MemorySearchEngine


class StubMemorySearchEngine(MemorySearchEngine):
    """Controllable Memory Platform search boundary."""

    def __init__(
        self,
        result: MemoryResult | None = None,
        error: Exception | None = None,
    ) -> None:
        self.result = result or MemoryResult()
        self.error = error
        self.last_query: MemoryQuery | None = None

    def search(
        self,
        query: MemoryQuery,
        memory_filter: Any = None,
    ) -> MemoryResult:
        self.last_query = query

        if self.error is not None:
            raise self.error

        return self.result


class InvalidResultSearchEngine(MemorySearchEngine):
    """Search engine returning an invalid result."""

    def search(
        self,
        query: MemoryQuery,
        memory_filter: Any = None,
    ) -> MemoryResult:
        return "invalid result"


def create_request(
    *,
    identity: IntelligenceIdentity | None = None,
    permission_constraints: tuple[str, ...] = (),
) -> IntelligenceRequest:
    return IntelligenceRequest(
        objective="Find JAOS architecture memories",
        request_type=IntelligenceRequestType.CONTEXT,
        identity=identity
        or IntelligenceIdentity(
            IntelligenceScope.USER,
            "vinay",
        ),
        permission_constraints=permission_constraints,
    )


def create_record(**overrides: Any) -> MemoryRecord:
    values: dict[str, Any] = {
        "memory_id": "memory-001",
        "content": "JAOS uses modular platform boundaries.",
        "memory_type": MemoryType.LONG_TERM,
        "identity": MemoryIdentity(
            MemoryScope.USER,
            "vinay",
        ),
        "source": "architecture-document",
        "importance": 0.9,
        "confidence": 0.95,
        "lifecycle_state": MemoryLifecycleState.ACTIVE,
        "metadata": MemoryMetadata(),
    }
    values.update(overrides)
    return MemoryRecord(**values)


def test_memory_context_source_lifecycle() -> None:
    source = MemoryContextSource(StubMemorySearchEngine())

    assert source.component_name == "context-source:memory-platform"
    assert source.source_name == "memory-platform"
    assert source.is_ready is False

    source.initialize()

    assert source.is_ready is True

    source.shutdown()

    assert source.is_ready is False


def test_memory_context_source_requires_ready_state() -> None:
    source = MemoryContextSource(StubMemorySearchEngine())

    with pytest.raises(IntelligenceComponentStateError):
        source.collect_context(create_request())


def test_memory_context_source_builds_scoped_query() -> None:
    engine = StubMemorySearchEngine()
    source = MemoryContextSource(
        engine,
        memory_types=(
            MemoryType.LONG_TERM,
            MemoryType.SEMANTIC,
        ),
        minimum_importance=0.4,
        minimum_confidence=0.5,
        max_results=5,
    )
    source.initialize()

    source.collect_context(create_request())

    query = engine.last_query

    assert query is not None
    assert query.query_text == "Find JAOS architecture memories"
    assert query.memory_types == (
        MemoryType.LONG_TERM,
        MemoryType.SEMANTIC,
    )
    assert query.scope is MemoryScope.USER
    assert query.identity == MemoryIdentity(
        MemoryScope.USER,
        "vinay",
    )
    assert query.minimum_importance == 0.4
    assert query.minimum_confidence == 0.5
    assert query.max_results == 5


def test_memory_context_source_maps_memory_record() -> None:
    record = create_record()
    engine = StubMemorySearchEngine(
        MemoryResult(
            records=[record],
            total_matches=1,
            query_time_ms=2.5,
        )
    )
    source = MemoryContextSource(engine)
    source.initialize()

    items = source.collect_context(create_request())

    assert len(items) == 1

    item = items[0]

    assert item.item_id == "memory:memory-001"
    assert item.context_type is IntelligenceContextType.MEMORY
    assert item.content == record.content
    assert item.identity == IntelligenceIdentity(
        IntelligenceScope.USER,
        "vinay",
    )
    assert item.source == "memory-platform"
    assert (
        item.trust_level
        is ContextTrustLevel.RETRIEVED_MEMORY
    )
    assert item.importance == 0.9
    assert item.confidence == 0.95
    assert item.metadata["memory_id"] == "memory-001"
    assert item.metadata["memory_type"] == "long_term"
    assert item.metadata["memory_query_time_ms"] == 2.5


def test_memory_context_source_allows_global_memory() -> None:
    record = create_record(
        identity=MemoryIdentity(MemoryScope.GLOBAL)
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert item.identity == IntelligenceIdentity(
        IntelligenceScope.GLOBAL
    )


def test_memory_context_source_rejects_identity_leak() -> None:
    record = create_record(
        identity=MemoryIdentity(
            MemoryScope.USER,
            "another-user",
        )
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_memory_context_source_rejects_unsupported_scope() -> None:
    source = MemoryContextSource(StubMemorySearchEngine())
    source.initialize()
    request = create_request(
        identity=IntelligenceIdentity(
            IntelligenceScope.PROJECT,
            "project-001",
        )
    )

    with pytest.raises(IntelligenceContextError):
        source.collect_context(request)


def test_memory_context_source_excludes_inactive_records() -> None:
    active = create_record(memory_id="active")
    archived = create_record(
        memory_id="archived",
        lifecycle_state=MemoryLifecycleState.ARCHIVED,
    )
    expired = create_record(
        memory_id="expired",
        lifecycle_state=MemoryLifecycleState.EXPIRED,
    )
    deleted = create_record(
        memory_id="deleted",
        lifecycle_state=MemoryLifecycleState.DELETED,
    )
    result = MemoryResult(
        records=[active, archived, expired, deleted],
        total_matches=4,
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(result)
    )
    source.initialize()

    items = source.collect_context(create_request())

    assert tuple(item.item_id for item in items) == (
        "memory:active",
    )


def test_memory_context_source_can_include_archived_records() -> None:
    active = create_record(memory_id="active")
    archived = create_record(
        memory_id="archived",
        lifecycle_state=MemoryLifecycleState.ARCHIVED,
    )
    result = MemoryResult(
        records=[active, archived],
        total_matches=2,
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(result),
        include_archived=True,
    )
    source.initialize()

    items = source.collect_context(create_request())

    assert tuple(item.item_id for item in items) == (
        "memory:active",
        "memory:archived",
    )


def test_memory_context_source_maps_permissions() -> None:
    record = create_record(
        metadata=MemoryMetadata(
            {
                "permission_constraints": [
                    " Memory.Read ",
                    "memory.read",
                ]
            }
        )
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert item.permission_constraints == ("memory.read",)


def test_memory_cannot_elevate_itself_to_required_context() -> None:
    record = create_record(
        metadata=MemoryMetadata(
            {
                "required_context": True,
                "security_constraint": True,
            }
        )
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert "required_context" not in item.metadata
    assert "security_constraint" not in item.metadata
    assert item.metadata["memory_metadata"] == {
        "required_context": True,
        "security_constraint": True,
    }


def test_memory_context_source_uses_stored_relevance() -> None:
    record = create_record(
        metadata=MemoryMetadata({"relevance": 0.72})
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    item = source.collect_context(create_request())[0]

    assert item.relevance == 0.72


def test_memory_context_source_wraps_search_failure() -> None:
    source = MemoryContextSource(
        StubMemorySearchEngine(
            error=RuntimeError("database unavailable")
        )
    )
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_memory_context_source_rejects_invalid_result() -> None:
    source = MemoryContextSource(InvalidResultSearchEngine())
    source.initialize()

    with pytest.raises(IntelligenceContextError):
        source.collect_context(create_request())


def test_memory_context_integrates_with_permission_filtering() -> None:
    record = create_record(
        metadata=MemoryMetadata(
            {"permission_constraints": ["memory.read"]}
        )
    )
    source = MemoryContextSource(
        StubMemorySearchEngine(
            MemoryResult(records=[record], total_matches=1)
        )
    )
    source.initialize()

    manager = DefaultIntelligenceContextManager()
    manager.register_source(source)
    manager.initialize()

    denied_bundle = manager.assemble_context(create_request())

    assert denied_bundle.items == ()
    assert denied_bundle.excluded_item_ids == (
        "memory:memory-001",
    )

    allowed_bundle = manager.assemble_context(
        create_request(
            permission_constraints=("memory.read",)
        )
    )

    assert len(allowed_bundle.items) == 1
    assert allowed_bundle.items[0].item_id == (
        "memory:memory-001"
    )


@pytest.mark.parametrize("max_results", [0, -1])
def test_memory_context_source_requires_positive_max_results(
    max_results: int,
) -> None:
    with pytest.raises(ValueError):
        MemoryContextSource(
            StubMemorySearchEngine(),
            max_results=max_results,
        )


def test_memory_context_source_requires_search_interface() -> None:
    with pytest.raises(TypeError):
        MemoryContextSource("invalid search engine")