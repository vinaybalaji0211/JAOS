from __future__ import annotations

import sqlite3
from pathlib import Path

from jaos.memory.providers.database_constants import (
    SCHEMA_VERSION,
    SQLITE_BUSY_TIMEOUT_MS,
    SQLITE_CACHE_SIZE,
    SQLITE_FOREIGN_KEYS,
    SQLITE_JOURNAL_MODE,
    SQLITE_PAGE_SIZE,
    SQLITE_SYNCHRONOUS,
    SQLITE_TEMP_STORE,
)

CREATE_SCHEMA_METADATA_TABLE = """
CREATE TABLE IF NOT EXISTS schema_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


CREATE_MEMORIES_TABLE = """
CREATE TABLE IF NOT EXISTS memories (
    memory_id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    memory_scope TEXT NOT NULL,
    identity_json TEXT NOT NULL,
    source TEXT NOT NULL,
    importance REAL NOT NULL,
    confidence REAL NOT NULL,
    lifecycle_state TEXT NOT NULL,
    metadata_json TEXT NOT NULL,
    statistics_json TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


CREATE_MEMORY_TYPE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_memory_type
ON memories(memory_type);
"""


CREATE_MEMORY_SCOPE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_memory_scope
ON memories(memory_scope);
"""


CREATE_LIFECYCLE_STATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_lifecycle_state
ON memories(lifecycle_state);
"""


CREATE_CREATED_AT_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_created_at
ON memories(created_at DESC);
"""


CREATE_UPDATED_AT_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_updated_at
ON memories(updated_at DESC);
"""


CREATE_IMPORTANCE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_importance
ON memories(importance DESC);
"""


CREATE_CONFIDENCE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_memories_confidence
ON memories(confidence DESC);
"""


SET_SCHEMA_VERSION = """
INSERT INTO schema_metadata (key, value)
VALUES ('schema_version', ?)
ON CONFLICT(key) DO UPDATE SET value = excluded.value;
"""


GET_SCHEMA_VERSION = """
SELECT value
FROM schema_metadata
WHERE key = 'schema_version';
"""


def create_sqlite_connection(
    database_path: str | Path,
) -> sqlite3.Connection:
    """
    Create and configure a SQLite connection for the memory platform.

    The caller owns the returned connection and must close it.

    Persistent database paths must be absolute. Relative paths are
    rejected before any directory is created or any connection is opened
    so memory state cannot resolve against the current working directory.
    """
    try:
        normalized_path = Path(database_path)

    except (TypeError, ValueError, OSError) as error:
        raise ValueError(
            "database_path must be ':memory:' or a valid absolute path"
        ) from error

    if str(normalized_path) != ":memory:":
        if not normalized_path.is_absolute():
            raise ValueError(
                "database_path must be an absolute path"
            )

        normalized_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        str(normalized_path),
        timeout=SQLITE_BUSY_TIMEOUT_MS / 1000.0,
        isolation_level=None,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    _configure_connection(connection)

    return connection


def initialize_sqlite_schema(
    connection: sqlite3.Connection,
) -> None:
    """
    Create or validate the SQLite memory schema.
    """
    connection.execute("BEGIN IMMEDIATE")

    try:
        connection.execute(CREATE_SCHEMA_METADATA_TABLE)

        existing_version = _read_schema_version(connection)

        if existing_version is not None and existing_version > SCHEMA_VERSION:
            raise RuntimeError(
                "SQLite memory schema version "
                f"{existing_version} is newer than supported version "
                f"{SCHEMA_VERSION}"
            )

        connection.execute(CREATE_MEMORIES_TABLE)
        connection.execute(CREATE_MEMORY_TYPE_INDEX)
        connection.execute(CREATE_MEMORY_SCOPE_INDEX)
        connection.execute(CREATE_LIFECYCLE_STATE_INDEX)
        connection.execute(CREATE_CREATED_AT_INDEX)
        connection.execute(CREATE_UPDATED_AT_INDEX)
        connection.execute(CREATE_IMPORTANCE_INDEX)
        connection.execute(CREATE_CONFIDENCE_INDEX)

        connection.execute(
            SET_SCHEMA_VERSION,
            (str(SCHEMA_VERSION),),
        )

        connection.commit()
    except BaseException:
        connection.rollback()
        raise


def get_sqlite_schema_version(
    connection: sqlite3.Connection,
) -> int | None:
    """
    Return the initialized schema version.

    Returns None when the schema metadata table does not exist or no version
    has been recorded.
    """
    try:
        return _read_schema_version(connection)
    except sqlite3.OperationalError:
        return None


def _configure_connection(
    connection: sqlite3.Connection,
) -> None:
    """
    Apply SQLite safety, concurrency, and performance configuration.
    """
    foreign_keys = "ON" if SQLITE_FOREIGN_KEYS else "OFF"

    connection.execute(
        f"PRAGMA busy_timeout = {SQLITE_BUSY_TIMEOUT_MS}"
    )
    connection.execute(
        f"PRAGMA foreign_keys = {foreign_keys}"
    )
    connection.execute(
        f"PRAGMA journal_mode = {SQLITE_JOURNAL_MODE}"
    )
    connection.execute(
        f"PRAGMA synchronous = {SQLITE_SYNCHRONOUS}"
    )
    connection.execute(
        f"PRAGMA temp_store = {SQLITE_TEMP_STORE}"
    )
    connection.execute(
        f"PRAGMA cache_size = {SQLITE_CACHE_SIZE}"
    )

    current_page_size = connection.execute(
        "PRAGMA page_size"
    ).fetchone()[0]

    if current_page_size != SQLITE_PAGE_SIZE:
        connection.execute(
            f"PRAGMA page_size = {SQLITE_PAGE_SIZE}"
        )


def _read_schema_version(
    connection: sqlite3.Connection,
) -> int | None:
    """
    Read and validate the current schema version.
    """
    row = connection.execute(GET_SCHEMA_VERSION).fetchone()

    if row is None:
        return None

    raw_version = row["value"]

    try:
        return int(raw_version)
    except (TypeError, ValueError) as error:
        raise RuntimeError(
            f"Invalid SQLite schema version: {raw_version!r}"
        ) from error