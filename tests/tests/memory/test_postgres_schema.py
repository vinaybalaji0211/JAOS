"""
JAOS Memory Platform

PostgreSQL Schema Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock, call, patch

import psycopg
import pytest
from psycopg import Connection
from psycopg.rows import dict_row

from jaos.memory.providers.database_constants import (
    SCHEMA_VERSION,
)
from jaos.memory.providers.postgres_schema import (
    CREATE_CONFIDENCE_INDEX,
    CREATE_CREATED_AT_INDEX,
    CREATE_IMPORTANCE_INDEX,
    CREATE_LIFECYCLE_STATE_INDEX,
    CREATE_MEMORIES_TABLE,
    CREATE_MEMORY_SCOPE_INDEX,
    CREATE_MEMORY_TYPE_INDEX,
    CREATE_SCHEMA_METADATA_TABLE,
    CREATE_UPDATED_AT_INDEX,
    GET_SCHEMA_VERSION,
    SET_SCHEMA_VERSION,
    _read_schema_version,
    _validate_connection_parameters,
    create_postgres_connection,
    get_postgres_schema_version,
    initialize_postgres_schema,
)


def create_mock_connection() -> MagicMock:
    """
    Create a mock PostgreSQL connection.
    """
    connection = MagicMock(spec=Connection)
    connection.closed = False
    return connection


def test_create_postgres_connection() -> None:
    parameters = {
        "host": "localhost",
        "port": 5432,
        "dbname": "jaos",
        "user": "postgres",
        "password": "secret",
    }

    expected_connection = create_mock_connection()

    with patch(
        "jaos.memory.providers.postgres_schema.psycopg.connect",
        return_value=expected_connection,
    ) as connect:
        result = create_postgres_connection(parameters)

    assert result is expected_connection

    connect.assert_called_once_with(
        **parameters,
        autocommit=False,
        row_factory=dict_row,
    )


def test_create_postgres_connection_does_not_modify_parameters() -> None:
    parameters = {
        "host": "localhost",
        "dbname": "jaos",
    }

    original_parameters = parameters.copy()

    with patch(
        "jaos.memory.providers.postgres_schema.psycopg.connect",
        return_value=create_mock_connection(),
    ):
        create_postgres_connection(parameters)

    assert parameters == original_parameters


@pytest.mark.parametrize(
    "connection_parameters",
    [
        None,
        "host=localhost",
        5432,
        ("localhost", 5432),
    ],
)
def test_create_connection_rejects_non_mapping(
    connection_parameters: object,
) -> None:
    with pytest.raises(
        TypeError,
        match="must be a mapping",
    ):
        create_postgres_connection(connection_parameters)


def test_create_connection_rejects_empty_parameters() -> None:
    with pytest.raises(
        ValueError,
        match="must not be empty",
    ):
        create_postgres_connection({})


@pytest.mark.parametrize(
    "managed_parameter",
    [
        "autocommit",
        "row_factory",
    ],
)
def test_create_connection_rejects_managed_parameters(
    managed_parameter: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="must not override",
    ):
        create_postgres_connection(
            {
                "host": "localhost",
                managed_parameter: True,
            }
        )


def test_validate_connection_parameters_returns_copy() -> None:
    original = {
        "host": "localhost",
        "dbname": "jaos",
    }

    result = _validate_connection_parameters(original)

    assert result == original
    assert result is not original


def test_initialize_postgres_schema() -> None:
    connection = create_mock_connection()

    schema_version_cursor = MagicMock()
    schema_version_cursor.fetchone.return_value = None

    default_cursor = MagicMock()

    def execute(
        statement: str,
        parameters: tuple[str, ...] | None = None,
    ) -> MagicMock:
        if statement == GET_SCHEMA_VERSION:
            return schema_version_cursor

        return default_cursor

    connection.execute.side_effect = execute

    initialize_postgres_schema(connection)

    assert connection.execute.call_args_list == [
        call(CREATE_SCHEMA_METADATA_TABLE),
        call(GET_SCHEMA_VERSION),
        call(CREATE_MEMORIES_TABLE),
        call(CREATE_MEMORY_TYPE_INDEX),
        call(CREATE_MEMORY_SCOPE_INDEX),
        call(CREATE_LIFECYCLE_STATE_INDEX),
        call(CREATE_CREATED_AT_INDEX),
        call(CREATE_UPDATED_AT_INDEX),
        call(CREATE_IMPORTANCE_INDEX),
        call(CREATE_CONFIDENCE_INDEX),
        call(
            SET_SCHEMA_VERSION,
            (str(SCHEMA_VERSION),),
        ),
    ]

    connection.commit.assert_called_once_with()
    connection.rollback.assert_not_called()


def test_initialize_schema_updates_existing_supported_version() -> None:
    connection = create_mock_connection()

    schema_version_cursor = MagicMock()
    schema_version_cursor.fetchone.return_value = {
        "value": str(SCHEMA_VERSION),
    }

    default_cursor = MagicMock()

    def execute(
        statement: str,
        parameters: tuple[str, ...] | None = None,
    ) -> MagicMock:
        if statement == GET_SCHEMA_VERSION:
            return schema_version_cursor

        return default_cursor

    connection.execute.side_effect = execute

    initialize_postgres_schema(connection)

    connection.execute.assert_any_call(
        SET_SCHEMA_VERSION,
        (str(SCHEMA_VERSION),),
    )
    connection.commit.assert_called_once_with()
    connection.rollback.assert_not_called()


def test_initialize_schema_rejects_newer_version() -> None:
    connection = create_mock_connection()

    schema_version_cursor = MagicMock()
    schema_version_cursor.fetchone.return_value = {
        "value": str(SCHEMA_VERSION + 1),
    }

    default_cursor = MagicMock()

    def execute(
        statement: str,
        parameters: tuple[str, ...] | None = None,
    ) -> MagicMock:
        if statement == GET_SCHEMA_VERSION:
            return schema_version_cursor

        return default_cursor

    connection.execute.side_effect = execute

    with pytest.raises(
        RuntimeError,
        match="newer than supported",
    ):
        initialize_postgres_schema(connection)

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once_with()


def test_initialize_schema_rolls_back_on_failure() -> None:
    connection = create_mock_connection()

    connection.execute.side_effect = RuntimeError(
        "database failure"
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        initialize_postgres_schema(connection)

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once_with()


def test_read_schema_version() -> None:
    connection = create_mock_connection()

    cursor = MagicMock()
    cursor.fetchone.return_value = {
        "value": "4",
    }

    connection.execute.return_value = cursor

    result = _read_schema_version(connection)

    assert result == 4

    connection.execute.assert_called_once_with(
        GET_SCHEMA_VERSION
    )


def test_read_schema_version_returns_none() -> None:
    connection = create_mock_connection()

    cursor = MagicMock()
    cursor.fetchone.return_value = None

    connection.execute.return_value = cursor

    result = _read_schema_version(connection)

    assert result is None


@pytest.mark.parametrize(
    "invalid_version",
    [
        "invalid",
        "",
        None,
        object(),
    ],
)
def test_read_schema_version_rejects_invalid_value(
    invalid_version: object,
) -> None:
    connection = create_mock_connection()

    cursor = MagicMock()
    cursor.fetchone.return_value = {
        "value": invalid_version,
    }

    connection.execute.return_value = cursor

    with pytest.raises(
        RuntimeError,
        match="Invalid PostgreSQL schema version",
    ):
        _read_schema_version(connection)


def test_get_postgres_schema_version() -> None:
    connection = create_mock_connection()

    cursor = MagicMock()
    cursor.fetchone.return_value = {
        "value": str(SCHEMA_VERSION),
    }

    connection.execute.return_value = cursor

    result = get_postgres_schema_version(connection)

    assert result == SCHEMA_VERSION


def test_get_schema_version_returns_none_for_missing_table() -> None:
    connection = create_mock_connection()

    connection.execute.side_effect = (
        psycopg.errors.UndefinedTable(
            "schema_metadata does not exist"
        )
    )

    result = get_postgres_schema_version(connection)

    assert result is None
    connection.rollback.assert_called_once_with()


def test_initialize_schema_rejects_invalid_connection() -> None:
    with pytest.raises(
        TypeError,
        match="psycopg Connection",
    ):
        initialize_postgres_schema(object())


def test_get_schema_version_rejects_invalid_connection() -> None:
    with pytest.raises(
        TypeError,
        match="psycopg Connection",
    ):
        get_postgres_schema_version(object())


def test_initialize_schema_rejects_closed_connection() -> None:
    connection = create_mock_connection()
    connection.closed = True

    with pytest.raises(
        RuntimeError,
        match="connection is closed",
    ):
        initialize_postgres_schema(connection)


def test_get_schema_version_rejects_closed_connection() -> None:
    connection = create_mock_connection()
    connection.closed = True

    with pytest.raises(
        RuntimeError,
        match="connection is closed",
    ):
        get_postgres_schema_version(connection)