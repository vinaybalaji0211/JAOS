"""
JAOS Memory Platform

PostgreSQL Transaction Tests
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from jaos.memory.providers.postgres_transaction import (
    PostgreSQLTransaction,
)
from jaos.memory.storage.memory_transaction import (
    MemoryTransaction,
)
from jaos.memory.storage.memory_writer import MemoryWriter


def create_mock_store() -> MagicMock:
    """
    Create a mock PostgreSQLStore-compatible object.
    """
    store = MagicMock()

    store._connection = MagicMock()

    store._validate_memory_id.side_effect = (
        lambda memory_id: memory_id.strip()
    )

    return store


def create_mock_record() -> MagicMock:
    """
    Create a mock memory record.
    """
    return MagicMock()


def test_transaction_implements_required_contracts() -> None:
    transaction = PostgreSQLTransaction(
        create_mock_store()
    )

    assert isinstance(
        transaction,
        MemoryTransaction,
    )
    assert isinstance(
        transaction,
        MemoryWriter,
    )


def test_enter_starts_transaction() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    result = transaction.__enter__()

    assert result is transaction
    assert transaction._active is True
    assert transaction._completed is False

    store._start_transaction.assert_called_once_with()


def test_context_manager_commits_successful_transaction() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    with transaction:
        pass

    store._start_transaction.assert_called_once_with()
    store._commit_transaction.assert_called_once_with()
    store._rollback_transaction.assert_not_called()

    assert transaction._active is False
    assert transaction._completed is True


def test_context_manager_rolls_back_after_exception() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    with pytest.raises(
        ValueError,
        match="operation failed",
    ), transaction:
        raise ValueError(
            "operation failed"
        )

    store._start_transaction.assert_called_once_with()
    store._commit_transaction.assert_not_called()
    store._rollback_transaction.assert_called_once_with()

    assert transaction._active is False
    assert transaction._completed is True


def test_context_manager_does_not_suppress_exception() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    transaction.__enter__()

    result = transaction.__exit__(
        RuntimeError,
        RuntimeError("failure"),
        None,
    )

    assert result is False


def test_enter_rejects_already_active_transaction() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    transaction.__enter__()

    with pytest.raises(
        RuntimeError,
        match="already active",
    ):
        transaction.__enter__()

    transaction.rollback()


def test_completed_transaction_cannot_be_reused() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    with transaction:
        pass

    with pytest.raises(
        RuntimeError,
        match="cannot be reused",
    ):
        transaction.__enter__()


def test_exit_completed_transaction_has_no_effect() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    with transaction:
        pass

    store._commit_transaction.reset_mock()
    store._rollback_transaction.reset_mock()

    result = transaction.__exit__(
        None,
        None,
        None,
    )

    assert result is False
    store._commit_transaction.assert_not_called()
    store._rollback_transaction.assert_not_called()


def test_create_persists_record_with_store_connection() -> None:
    store = create_mock_store()
    record = create_mock_record()

    store._create_with_connection.return_value = record

    transaction = PostgreSQLTransaction(store)

    with transaction:
        result = transaction.create(record)

    assert result is record

    store._create_with_connection.assert_called_once_with(
        store._connection,
        record,
    )


def test_update_replaces_record_with_store_connection() -> None:
    store = create_mock_store()
    record = create_mock_record()

    store._update_with_connection.return_value = record

    transaction = PostgreSQLTransaction(store)

    with transaction:
        result = transaction.update(record)

    assert result is record

    store._update_with_connection.assert_called_once_with(
        store._connection,
        record,
    )


def test_delete_validates_and_deletes_memory() -> None:
    store = create_mock_store()

    store._delete_with_connection.return_value = True

    transaction = PostgreSQLTransaction(store)

    with transaction:
        result = transaction.delete(
            " memory-001 "
        )

    assert result is True

    store._validate_memory_id.assert_called_once_with(
        " memory-001 "
    )

    store._delete_with_connection.assert_called_once_with(
        store._connection,
        "memory-001",
    )


def test_clear_deletes_all_memories() -> None:
    store = create_mock_store()

    store._clear_with_connection.return_value = 12

    transaction = PostgreSQLTransaction(store)

    with transaction:
        result = transaction.clear()

    assert result == 12

    store._clear_with_connection.assert_called_once_with(
        store._connection
    )


@pytest.mark.parametrize(
    "operation",
    [
        "create",
        "update",
        "delete",
        "clear",
        "commit",
        "rollback",
    ],
)
def test_operations_require_active_transaction(
    operation: str,
) -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)
    record = create_mock_record()

    with pytest.raises(
        RuntimeError,
        match="transaction is not active",
    ):
        if operation == "create":
            transaction.create(record)
        elif operation == "update":
            transaction.update(record)
        elif operation == "delete":
            transaction.delete("memory-001")
        elif operation == "clear":
            transaction.clear()
        elif operation == "commit":
            transaction.commit()
        else:
            transaction.rollback()


def test_manual_commit_completes_transaction() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    transaction.__enter__()
    transaction.commit()

    store._commit_transaction.assert_called_once_with()
    store._rollback_transaction.assert_not_called()

    assert transaction._active is False
    assert transaction._completed is True


def test_manual_rollback_completes_transaction() -> None:
    store = create_mock_store()
    transaction = PostgreSQLTransaction(store)

    transaction.__enter__()
    transaction.rollback()

    store._commit_transaction.assert_not_called()
    store._rollback_transaction.assert_called_once_with()

    assert transaction._active is False
    assert transaction._completed is True


def test_commit_finishes_transaction_when_store_commit_fails() -> None:
    store = create_mock_store()

    store._commit_transaction.side_effect = RuntimeError(
        "commit failed"
    )

    transaction = PostgreSQLTransaction(store)
    transaction.__enter__()

    with pytest.raises(
        RuntimeError,
        match="commit failed",
    ):
        transaction.commit()

    assert transaction._active is False
    assert transaction._completed is True


def test_rollback_finishes_transaction_when_store_rollback_fails() -> None:
    store = create_mock_store()

    store._rollback_transaction.side_effect = RuntimeError(
        "rollback failed"
    )

    transaction = PostgreSQLTransaction(store)
    transaction.__enter__()

    with pytest.raises(
        RuntimeError,
        match="rollback failed",
    ):
        transaction.rollback()

    assert transaction._active is False
    assert transaction._completed is True