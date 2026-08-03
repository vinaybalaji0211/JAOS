"""
JAOS Memory Platform

PostgreSQL Schema

Creates PostgreSQL connections and initializes the persistent memory schema.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import psycopg
from psycopg import Connection
from psycopg.rows import dict_row

from jaos.memory.providers.database_constants import (
    SCHEMA_VERSION,
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
    importance DOUBLE PRECISION NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
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
VALUES ('schema_version', %s)
ON CONFLICT(key) DO UPDATE
SET value = EXCLUDED.value;
"""


GET_SCHEMA_VERSION = """
SELECT value
FROM schema_metadata
WHERE key = 'schema_version';
"""


def create_postgres_connection(
    connection_parameters: Mapping[str, Any],
) -> Connection[dict[str, Any]]:
    """
    Create and configure a PostgreSQL connection.

    Args:
        connection_parameters:
            Keyword arguments accepted by psycopg.connect(), such as host,
            port, dbname, user, password, sslmode, and connect_timeout.

    Returns:
        An open PostgreSQL connection configured to return dictionary rows.

    The caller owns the returned connection and must close it.
    """
    normalized_parameters = _validate_connection_parameters(
        connection_parameters
    )

    connection = psycopg.connect(
        **normalized_parameters,
        autocommit=False,
        row_factory=dict_row,
    )

    return connection


def initialize_postgres_schema(
    connection: Connection[dict[str, Any]],
) -> None:
    """
    Create or validate the PostgreSQL memory schema.

    Schema initialization is atomic. Any failure rolls back every change
    performed during the initialization attempt.
    """
    _validate_connection(connection)

    try:
        connection.execute(CREATE_SCHEMA_METADATA_TABLE)

        existing_version = _read_schema_version(connection)

        if (
            existing_version is not None
            and existing_version > SCHEMA_VERSION
        ):
            raise RuntimeError(
                "PostgreSQL memory schema version "
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


def get_postgres_schema_version(
    connection: Connection[dict[str, Any]],
) -> int | None:
    """
    Return the initialized PostgreSQL schema version.

    Returns None when the schema metadata table does not exist or when no
    schema version has been recorded.
    """
    _validate_connection(connection)

    try:
        return _read_schema_version(connection)
    except psycopg.errors.UndefinedTable:
        connection.rollback()
        return None


def _read_schema_version(
    connection: Connection[dict[str, Any]],
) -> int | None:
    """
    Read and validate the current PostgreSQL schema version.
    """
    row = connection.execute(
        GET_SCHEMA_VERSION
    ).fetchone()

    if row is None:
        return None

    raw_version = row["value"]

    try:
        return int(raw_version)
    except (TypeError, ValueError) as error:
        raise RuntimeError(
            "Invalid PostgreSQL schema version: "
            f"{raw_version!r}"
        ) from error


def _validate_connection_parameters(
    connection_parameters: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Validate and copy PostgreSQL connection parameters.
    """
    if not isinstance(connection_parameters, Mapping):
        raise TypeError(
            "connection_parameters must be a mapping"
        )

    normalized_parameters = dict(connection_parameters)

    if not normalized_parameters:
        raise ValueError(
            "connection_parameters must not be empty"
        )

    managed_parameters = {
        "autocommit",
        "row_factory",
    }

    conflicting_parameters = managed_parameters.intersection(
        normalized_parameters
    )

    if conflicting_parameters:
        conflicting_names = ", ".join(
            sorted(conflicting_parameters)
        )

        raise ValueError(
            "connection_parameters must not override managed "
            f"parameters: {conflicting_names}"
        )

    return normalized_parameters


def _validate_connection(
    connection: Connection[dict[str, Any]],
) -> None:
    """
    Validate a PostgreSQL connection object.
    """
    if not isinstance(connection, Connection):
        raise TypeError(
            "connection must be a psycopg Connection"
        )

    if connection.closed:
        raise RuntimeError(
            "PostgreSQL connection is closed"
        )