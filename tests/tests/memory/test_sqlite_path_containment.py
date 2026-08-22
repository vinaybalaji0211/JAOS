"""FORTRESS-02H containment tests for canonical SQLite memory paths.

Persistent memory paths must be absolute so provider state cannot
resolve against the current working directory or the repository tree.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from jaos.memory.providers.database_constants import (
    DEFAULT_DATABASE_FILENAME,
)
from jaos.memory.providers.sqlite_provider import SQLiteProvider
from jaos.memory.providers.sqlite_schema import (
    create_sqlite_connection,
    initialize_sqlite_schema,
)


_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

_RELATIVE_PATHS = (
    "memory.sqlite3",
    "./memory.sqlite3",
    "state/memory.sqlite3",
    "data/memory/memory.sqlite3",
)


@pytest.mark.parametrize("relative_path", _RELATIVE_PATHS)
def test_provider_rejects_relative_database_paths(
    relative_path: str,
) -> None:
    """S1: the bare constructor refuses relative database paths."""

    with pytest.raises(ValueError):
        SQLiteProvider(relative_path)


def test_provider_accepts_absolute_database_path(
    tmp_path: Path,
) -> None:
    """S2: absolute paths remain valid and are preserved verbatim."""

    database_path = tmp_path / "memory" / "memory.sqlite3"

    provider = SQLiteProvider(database_path)

    assert provider.database_path == database_path
    assert provider.database_path.is_absolute()


def test_from_memory_scope_still_binds_injected_scope(
    tmp_path: Path,
) -> None:
    """S3: the 02E entry point is unchanged."""

    memory_scope = tmp_path / "runtime" / "memory"

    provider = SQLiteProvider.from_memory_scope(memory_scope)

    assert provider.database_path == (
        memory_scope / DEFAULT_DATABASE_FILENAME
    )

    provider.initialize()

    assert memory_scope.is_dir()


@pytest.mark.parametrize("relative_path", _RELATIVE_PATHS)
def test_connection_factory_rejects_relative_paths(
    relative_path: str,
) -> None:
    """S4: rejection happens before mkdir and before sqlite3.connect."""

    with pytest.raises(ValueError):
        create_sqlite_connection(relative_path)


@pytest.mark.parametrize("relative_path", _RELATIVE_PATHS)
def test_rejected_relative_path_creates_no_artifact(
    relative_path: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    protected_repository_state: None,
) -> None:
    """S5: a rejected path leaves no directory or database behind."""

    monkeypatch.chdir(tmp_path)

    with pytest.raises(ValueError):
        create_sqlite_connection(relative_path)

    with pytest.raises(ValueError):
        SQLiteProvider(relative_path)

    assert list(tmp_path.iterdir()) == []


def test_absolute_path_supports_schema_initialization(
    tmp_path: Path,
) -> None:
    """S6: absolute paths still initialize the schema and close cleanly."""

    database_path = tmp_path / "memory" / "memory.sqlite3"

    connection = create_sqlite_connection(database_path)

    try:
        initialize_sqlite_schema(connection)

        cursor = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
        table_names = {row["name"] for row in cursor.fetchall()}

    finally:
        connection.close()

    assert table_names
    assert database_path.is_file()


def test_in_memory_database_remains_supported() -> None:
    """S6: the pre-existing ':memory:' path is preserved."""

    connection = create_sqlite_connection(":memory:")

    try:
        initialize_sqlite_schema(connection)
        assert isinstance(connection, sqlite3.Connection)

    finally:
        connection.close()


def test_wal_and_shm_handles_close_cleanly(
    tmp_path: Path,
) -> None:
    """S9: no write-ahead artifacts survive a clean close."""

    database_path = tmp_path / "memory" / "memory.sqlite3"

    connection = create_sqlite_connection(database_path)

    try:
        initialize_sqlite_schema(connection)

    finally:
        connection.close()

    lingering = [
        entry.name
        for entry in database_path.parent.iterdir()
        if entry.name.endswith("-wal") or entry.name.endswith("-shm")
    ]

    assert lingering == []


def test_no_sqlite_database_exists_inside_repository() -> None:
    """S10: the repository tree holds no SQLite database artifact."""

    skipped_directories = {".git", ".venv"}
    suffixes = ("-wal", "-shm", ".sqlite3", ".sqlite", ".db")
    discovered: list[str] = []

    for entry in _REPOSITORY_ROOT.rglob("*"):
        if any(part in skipped_directories for part in entry.parts):
            continue
        if not entry.is_file():
            continue
        if entry.name.endswith(suffixes):
            discovered.append(str(entry.relative_to(_REPOSITORY_ROOT)))

    assert discovered == []
