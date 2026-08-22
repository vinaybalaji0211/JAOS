"""FORTRESS-02E tests for canonical Memory persistence-path binding."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import pytest

from jaos.memory.models.memory_identity import MemoryIdentity
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_scope import MemoryScope
from jaos.memory.models.memory_type import MemoryType
from jaos.memory.providers.database_constants import (
    DEFAULT_DATABASE_FILENAME,
)
from jaos.memory.providers.provider_factory import ProviderFactory
from jaos.memory.providers.provider_registry import ProviderRegistry
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.providers.sqlite_store import SQLiteStore
from jaos_platform.runtime_paths import RuntimePaths


RuntimePathsFactory = Callable[[Path], RuntimePaths]


def _build_record(memory_id: str, content: str) -> MemoryRecord:
    return MemoryRecord(
        memory_id=memory_id,
        content=content,
        memory_type=next(iter(MemoryType)),
        identity=MemoryIdentity(scope=MemoryScope.GLOBAL),
        source="fortress-02e-test",
    )


def _open_canonical_store(
    runtime_paths: RuntimePaths,
) -> tuple[SQLiteProvider, SQLiteStore]:
    provider = SQLiteProvider.from_memory_scope(runtime_paths.memory)
    registry = ProviderRegistry()
    registry.register(provider)
    store = ProviderFactory(registry).create_default()
    assert isinstance(store, SQLiteStore)
    return provider, store


def test_binding_derives_canonical_sqlite_path_without_side_effects(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    provider = SQLiteProvider.from_memory_scope(
        jaos_runtime_paths.memory
    )

    assert DEFAULT_DATABASE_FILENAME == "memory.sqlite3"
    assert provider.database_path == (
        jaos_runtime_paths.memory / "memory.sqlite3"
    )
    assert not jaos_runtime_paths.memory.exists()
    assert not provider.database_path.exists()


@pytest.mark.parametrize(
    "invalid_scope",
    ("", "relative/memory", Path("relative-memory"), None, 42),
)
def test_binding_rejects_invalid_or_relative_memory_scopes(
    invalid_scope: object,
) -> None:
    with pytest.raises(
        ValueError,
        match="memory_scope must be .*absolute path",
    ):
        SQLiteProvider.from_memory_scope(invalid_scope)  # type: ignore[arg-type]


def test_distinct_runtime_paths_use_isolated_databases(
    tmp_path: Path,
    jaos_runtime_paths_factory: RuntimePathsFactory,
) -> None:
    first_paths = jaos_runtime_paths_factory(tmp_path / "first")
    second_paths = jaos_runtime_paths_factory(tmp_path / "second")
    first_provider, first_store = _open_canonical_store(first_paths)
    second_provider, second_store = _open_canonical_store(second_paths)

    try:
        first_store.create(_build_record("first", "first runtime"))

        assert first_provider.database_path != second_provider.database_path
        assert first_store.count() == 1
        assert second_store.count() == 0
    finally:
        first_store.close()
        second_store.close()


def test_binding_ignores_cwd_and_runtime_environment(
    tmp_path: Path,
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    working_directory = tmp_path / "unrelated-working-directory"
    working_directory.mkdir()
    monkeypatch.chdir(working_directory)
    monkeypatch.setenv("JAOS_RUNTIME_DIR", "relative-must-not-be-read")

    provider = SQLiteProvider.from_memory_scope(
        jaos_runtime_paths.memory
    )

    assert provider.database_path == (
        jaos_runtime_paths.memory / "memory.sqlite3"
    )
    assert not (working_directory / "memory.sqlite3").exists()


def test_initialization_writes_only_to_injected_memory_scope(
    jaos_runtime_paths: RuntimePaths,
    protected_repository_state: None,
) -> None:
    provider, store = _open_canonical_store(jaos_runtime_paths)

    try:
        assert provider.database_path.is_file()
        assert provider.database_path.parent == jaos_runtime_paths.memory
        created_paths = tuple(jaos_runtime_paths.memory.iterdir())
        assert provider.database_path in created_paths
        assert all(
            path.parent == jaos_runtime_paths.memory
            for path in created_paths
        )
        assert not jaos_runtime_paths.state.exists()
        assert not jaos_runtime_paths.logs.exists()
    finally:
        store.close()


def test_canonical_store_preserves_crud_and_reopen_persistence(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    provider, first_store = _open_canonical_store(jaos_runtime_paths)
    record = _build_record("persistent", "survives reopen")

    first_store.create(record)
    assert first_store.get(record.memory_id) == record
    first_store.close()

    second_store = provider.create_store()
    try:
        assert second_store.get(record.memory_id) == record
        assert second_store.count() == 1
    finally:
        second_store.close()


def test_canonical_store_preserves_transaction_commit_and_rollback(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    _, store = _open_canonical_store(jaos_runtime_paths)
    committed = _build_record("committed", "commit me")
    rolled_back = _build_record("rolled-back", "discard me")

    try:
        with store.begin_transaction() as transaction:
            transaction.create(committed)

        transaction = store.begin_transaction()
        transaction.__enter__()
        transaction.create(rolled_back)
        transaction.rollback()

        assert store.get(committed.memory_id) == committed
        assert store.get(rolled_back.memory_id) is None
    finally:
        store.close()


def test_closed_store_releases_sqlite_files(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    provider, store = _open_canonical_store(jaos_runtime_paths)
    database_path = provider.database_path
    wal_path = Path(f"{database_path}-wal")
    shm_path = Path(f"{database_path}-shm")

    store.create(_build_record("close", "release handles"))
    store.close()

    assert store.is_closed
    assert not wal_path.exists()
    assert not shm_path.exists()
    database_path.unlink()
    assert not database_path.exists()


def test_legacy_json_is_not_used_as_a_fallback(
    tmp_path: Path,
    jaos_runtime_paths: RuntimePaths,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    working_directory = tmp_path / "legacy-working-directory"
    legacy_path = (
        working_directory / "data" / "memory" / "long_term_memory.json"
    )
    legacy_path.parent.mkdir(parents=True)
    legacy_path.write_text(
        json.dumps({"memories": [{"memory_id": "legacy"}]}),
        encoding="utf-8",
    )
    monkeypatch.chdir(working_directory)

    provider, store = _open_canonical_store(jaos_runtime_paths)
    try:
        assert provider.database_path == (
            jaos_runtime_paths.memory / "memory.sqlite3"
        )
        assert store.count() == 0
        assert store.get("legacy") is None
    finally:
        store.close()


def test_each_function_scoped_runtime_starts_without_database(
    jaos_runtime_paths: RuntimePaths,
) -> None:
    database_path = jaos_runtime_paths.memory / "memory.sqlite3"

    assert not database_path.exists()
