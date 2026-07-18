from __future__ import annotations

from dataclasses import replace

import pytest

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.providers.in_memory_store import InMemoryStore


@pytest.fixture
def memory_type() -> MemoryType:
    """
    Return one valid memory type without depending on a specific enum member.
    """
    return next(iter(MemoryType))


@pytest.fixture
def second_memory_type(memory_type: MemoryType) -> MemoryType:
    """
    Return another valid memory type when available.
    """
    for candidate in MemoryType:
        if candidate != memory_type:
            return candidate

    return memory_type


@pytest.fixture
def global_identity() -> MemoryIdentity:
    """
    Return a valid global memory identity.
    """
    return MemoryIdentity(scope=MemoryScope.GLOBAL)


def build_record(
    *,
    content: str,
    memory_type: MemoryType,
    identity: MemoryIdentity,
    memory_id: str,
    importance: float = 0.5,
    confidence: float = 1.0,
    tags: tuple[str, ...] = (),
) -> MemoryRecord:
    """
    Build a valid memory record for provider tests.
    """
    return MemoryRecord(
        memory_id=memory_id,
        content=content,
        memory_type=memory_type,
        identity=identity,
        source="unit-test",
        importance=importance,
        confidence=confidence,
        metadata=MemoryMetadata(
            values={
                "tags": tags,
            }
        ),
    )


def test_store_starts_empty() -> None:
    store = InMemoryStore()

    assert store.count() == 0
    assert store.list_records().records == []
    assert store.list_records().total_matches == 0


def test_create_and_get_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="JAOS remembers project architecture.",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="memory-001",
    )

    created = store.create(record)

    assert created == record
    assert store.get("memory-001") == record
    assert store.count() == 1


def test_create_rejects_duplicate_memory_id(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="Original memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="duplicate-id",
    )

    store.create(record)

    with pytest.raises(
        ValueError,
        match="Memory record already exists",
    ):
        store.create(record)


def test_get_returns_none_for_unknown_memory() -> None:
    store = InMemoryStore()

    assert store.get("missing-memory") is None


def test_update_replaces_existing_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    original = build_record(
        content="Original content",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="memory-update",
        importance=0.4,
    )
    updated = replace(
        original,
        content="Updated content",
        importance=0.9,
    )

    store.create(original)
    result = store.update(updated)

    assert result == updated
    assert store.get("memory-update") == updated
    assert store.count() == 1


def test_update_rejects_unknown_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="Unknown record",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="unknown-id",
    )

    with pytest.raises(
        ValueError,
        match="Memory record does not exist",
    ):
        store.update(record)


def test_delete_existing_record(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="Delete this memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="memory-delete",
    )

    store.create(record)

    assert store.delete("memory-delete") is True
    assert store.get("memory-delete") is None
    assert store.count() == 0


def test_delete_unknown_record_returns_false() -> None:
    store = InMemoryStore()

    assert store.delete("unknown-memory") is False


def test_list_records_returns_all_records(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    first = build_record(
        content="First memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="list-001",
    )
    second = build_record(
        content="Second memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="list-002",
    )

    store.create(first)
    store.create(second)

    result = store.list_records()

    assert result.total_matches == 2
    assert {record.memory_id for record in result.records} == {
    first.memory_id,
    second.memory_id,
}
    assert result.query_time_ms >= 0.0


def test_list_records_supports_pagination(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    for index in range(5):
        store.create(
            build_record(
                content=f"Paginated memory {index}",
                memory_type=memory_type,
                identity=global_identity,
                memory_id=f"page-{index}",
            )
        )

    first_page = store.list_records(limit=2, offset=0)
    second_page = store.list_records(limit=2, offset=2)

    assert first_page.total_matches == 5
    assert second_page.total_matches == 5
    assert len(first_page.records) == 2
    assert len(second_page.records) == 2

    first_page_ids = {
        record.memory_id for record in first_page.records
    }
    second_page_ids = {
        record.memory_id for record in second_page.records
    }

    assert first_page_ids.isdisjoint(second_page_ids)


@pytest.mark.parametrize(
    ("limit", "exception_type"),
    [
        (0, ValueError),
        (-1, ValueError),
        (1.5, TypeError),
    ],
)
def test_list_records_validates_limit(
    limit: object,
    exception_type: type[Exception],
) -> None:
    store = InMemoryStore()

    with pytest.raises(exception_type):
        store.list_records(limit=limit)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("offset", "exception_type"),
    [
        (-1, ValueError),
        (1.5, TypeError),
    ],
)
def test_list_records_validates_offset(
    offset: object,
    exception_type: type[Exception],
) -> None:
    store = InMemoryStore()

    with pytest.raises(exception_type):
        store.list_records(offset=offset)  # type: ignore[arg-type]


def test_filter_by_memory_type(
    memory_type: MemoryType,
    second_memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    if second_memory_type == memory_type:
        pytest.skip("MemoryType contains only one enum member")

    store = InMemoryStore()

    matching = build_record(
        content="Matching memory type",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="type-match",
    )
    non_matching = build_record(
        content="Different memory type",
        memory_type=second_memory_type,
        identity=global_identity,
        memory_id="type-other",
    )

    store.create(matching)
    store.create(non_matching)

    result = store.list_records(
        MemoryFilter(memory_type=memory_type)
    )

    assert result.total_matches == 1
    assert result.records == [matching]
    assert store.count(
        MemoryFilter(memory_type=memory_type)
    ) == 1


def test_filter_by_scope(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="Global scoped memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="scope-global",
    )

    store.create(record)

    result = store.list_records(
        MemoryFilter(memory_scope=MemoryScope.GLOBAL)
    )

    assert result.total_matches == 1
    assert result.records == [record]


def test_filter_by_minimum_importance(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    low = build_record(
        content="Low importance memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="importance-low",
        importance=0.2,
    )
    high = build_record(
        content="High importance memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="importance-high",
        importance=0.9,
    )

    store.create(low)
    store.create(high)

    result = store.list_records(
        MemoryFilter(minimum_importance=0.8)
    )

    assert result.total_matches == 1
    assert result.records == [high]


def test_filter_by_tags(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    matching = build_record(
        content="Tagged architecture memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="tag-match",
        tags=("jaos", "architecture"),
    )
    non_matching = build_record(
        content="Unrelated tagged memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="tag-other",
        tags=("personal",),
    )

    store.create(matching)
    store.create(non_matching)

    result = store.list_records(
        MemoryFilter(tags=("jaos", "architecture"))
    )

    assert result.total_matches == 1
    assert result.records == [matching]


def test_search_is_case_insensitive(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()
    record = build_record(
        content="JAOS Memory Platform Architecture",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="search-case",
    )

    store.create(record)

    result = store.search(
        MemoryQuery(query_text="memory platform")
    )

    assert result.total_matches == 1
    assert result.records == [record]
    assert result.query_time_ms >= 0.0


def test_search_applies_query_criteria(
    memory_type: MemoryType,
    second_memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    matching = build_record(
        content="JAOS provider architecture",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="query-match",
        importance=0.9,
        confidence=0.95,
    )
    low_confidence = build_record(
        content="JAOS provider architecture",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="query-low-confidence",
        importance=0.9,
        confidence=0.3,
    )

    store.create(matching)
    store.create(low_confidence)

    query = MemoryQuery(
        query_text="provider",
        memory_types=(memory_type,),
        scope=MemoryScope.GLOBAL,
        minimum_importance=0.8,
        minimum_confidence=0.8,
    )

    result = store.search(query)

    assert result.total_matches == 1
    assert result.records == [matching]


def test_search_applies_optional_memory_filter(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    architecture = build_record(
        content="JAOS memory architecture",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="search-tag-match",
        tags=("architecture",),
    )
    implementation = build_record(
        content="JAOS memory implementation",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="search-tag-other",
        tags=("implementation",),
    )

    store.create(architecture)
    store.create(implementation)

    result = store.search(
        MemoryQuery(query_text="JAOS"),
        MemoryFilter(tags=("architecture",)),
    )

    assert result.total_matches == 1
    assert result.records == [architecture]


def test_search_respects_max_results(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    for index in range(5):
        store.create(
            build_record(
                content=f"JAOS searchable memory {index}",
                memory_type=memory_type,
                identity=global_identity,
                memory_id=f"search-limit-{index}",
                importance=0.5 + (index * 0.1),
            )
        )

    result = store.search(
        MemoryQuery(
            query_text="JAOS",
            max_results=2,
        )
    )

    assert result.total_matches == 5
    assert len(result.records) == 2


def test_search_orders_by_importance_then_confidence(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    lower = build_record(
        content="JAOS ranking memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="ranking-low",
        importance=0.6,
        confidence=1.0,
    )
    higher = build_record(
        content="JAOS ranking memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="ranking-high",
        importance=0.9,
        confidence=0.8,
    )

    store.create(lower)
    store.create(higher)

    result = store.search(
        MemoryQuery(query_text="ranking")
    )

    assert result.records == [higher, lower]


def test_clear_removes_all_records(
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    store = InMemoryStore()

    store.create(
        build_record(
            content="First clear memory",
            memory_type=memory_type,
            identity=global_identity,
            memory_id="clear-001",
        )
    )
    store.create(
        build_record(
            content="Second clear memory",
            memory_type=memory_type,
            identity=global_identity,
            memory_id="clear-002",
        )
    )

    deleted_count = store.clear()

    assert deleted_count == 2
    assert store.count() == 0
    assert store.clear() == 0