from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_metadata import MemoryMetadata
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.providers.sqlite_store import SQLiteStore


@pytest.fixture
def memory_type() -> MemoryType:
    """
    Return one valid memory type.
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
    Return a valid global identity.
    """
    return MemoryIdentity(scope=MemoryScope.GLOBAL)


@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    """
    Return an isolated SQLite database path.
    """
    return tmp_path / "jaos-memory-test.db"


@pytest.fixture
def store(database_path: Path) -> SQLiteStore:
    """
    Return an isolated SQLiteStore and close it after the test.
    """
    sqlite_store = SQLiteStore(database_path)

    try:
        yield sqlite_store
    finally:
        if not sqlite_store.is_closed:
            sqlite_store.close()


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
    Build a valid memory record for SQLite provider tests.
    """
    return MemoryRecord(
        memory_id=memory_id,
        content=content,
        memory_type=memory_type,
        identity=identity,
        source="sqlite-unit-test",
        importance=importance,
        confidence=confidence,
        metadata=MemoryMetadata(
            values={
                "tags": tags,
            }
        ),
    )


def test_store_starts_empty(store: SQLiteStore) -> None:
    assert store.count() == 0
    assert store.list_records().records == []
    assert store.list_records().total_matches == 0


def test_create_and_get_record(
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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


def test_get_returns_none_for_unknown_memory(
    store: SQLiteStore,
) -> None:
    assert store.get("missing-memory") is None


@pytest.mark.parametrize(
    ("memory_id", "exception_type"),
    [
        ("", ValueError),
        ("   ", ValueError),
        (123, TypeError),
    ],
)
def test_get_validates_memory_id(
    store: SQLiteStore,
    memory_id: object,
    exception_type: type[Exception],
) -> None:
    with pytest.raises(exception_type):
        store.get(memory_id)  # type: ignore[arg-type]


def test_update_replaces_existing_record(
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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


def test_delete_unknown_record_returns_false(
    store: SQLiteStore,
) -> None:
    assert store.delete("unknown-memory") is False


def test_list_records_returns_all_records(
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    assert {
        record.memory_id for record in result.records
    } == {
        first.memory_id,
        second.memory_id,
    }
    assert result.query_time_ms >= 0.0


def test_list_records_supports_pagination(
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    limit: object,
    exception_type: type[Exception],
) -> None:
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
    store: SQLiteStore,
    offset: object,
    exception_type: type[Exception],
) -> None:
    with pytest.raises(exception_type):
        store.list_records(offset=offset)  # type: ignore[arg-type]


def test_filter_by_memory_type(
    store: SQLiteStore,
    memory_type: MemoryType,
    second_memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    if second_memory_type == memory_type:
        pytest.skip("MemoryType contains only one enum member")

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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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


def test_search_filters_by_exact_identity(
    store: SQLiteStore,
    memory_type: MemoryType,
) -> None:
    first_identity = MemoryIdentity(
        scope=MemoryScope.USER,
        identity_id="user-001",
    )
    second_identity = MemoryIdentity(
        scope=MemoryScope.USER,
        identity_id="user-002",
    )

    matching = build_record(
        content="JAOS user preference memory",
        memory_type=memory_type,
        identity=first_identity,
        memory_id="identity-match",
    )
    non_matching = build_record(
        content="JAOS user preference memory",
        memory_type=memory_type,
        identity=second_identity,
        memory_id="identity-other",
    )

    store.create(matching)
    store.create(non_matching)

    result = store.search(
        MemoryQuery(
            query_text="preference",
            identity=first_identity,
        )
    )

    assert result.total_matches == 1
    assert result.records == [matching]


def test_search_applies_optional_memory_filter(
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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
    store: SQLiteStore,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
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


def test_records_persist_after_provider_restart(
    database_path: Path,
    memory_type: MemoryType,
    global_identity: MemoryIdentity,
) -> None:
    record = build_record(
        content="Persistent SQLite memory",
        memory_type=memory_type,
        identity=global_identity,
        memory_id="persistent-memory",
        tags=("sqlite", "persistent"),
    )

    first_store = SQLiteStore(database_path)
    first_store.create(record)
    first_store.close()

    second_store = SQLiteStore(database_path)

    try:
        assert second_store.get(record.memory_id) == record
        assert second_store.count() == 1
    finally:
        second_store.close()


def test_context_manager_closes_store(
    database_path: Path,
) -> None:
    with SQLiteStore(database_path) as context_store:
        assert context_store.is_closed is False

    assert context_store.is_closed is True


def test_close_is_idempotent(
    database_path: Path,
) -> None:
    sqlite_store = SQLiteStore(database_path)

    sqlite_store.close()
    sqlite_store.close()

    assert sqlite_store.is_closed is True


def test_operations_fail_after_store_is_closed(
    database_path: Path,
) -> None:
    sqlite_store = SQLiteStore(database_path)
    sqlite_store.close()

    with pytest.raises(RuntimeError, match="SQLiteStore is closed"):
        sqlite_store.count()

    with pytest.raises(RuntimeError, match="SQLiteStore is closed"):
        sqlite_store.list_records()

    with pytest.raises(RuntimeError, match="SQLiteStore is closed"):
        sqlite_store.get("closed-memory")


@pytest.mark.parametrize(
    "invalid_path",
    [
        "",
        "   ",
    ],
)
def test_store_rejects_empty_database_path(
    invalid_path: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="database_path must not be empty",
    ):
        SQLiteStore(invalid_path)


def test_store_rejects_invalid_database_path_type() -> None:
    with pytest.raises(
        TypeError,
        match="database_path must be",
    ):
        SQLiteStore(123)  # type: ignore[arg-type]