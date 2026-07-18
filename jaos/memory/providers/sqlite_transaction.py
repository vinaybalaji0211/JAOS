from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Self

from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.storage.memory_transaction import MemoryTransaction
from jaos.memory.storage.memory_writer import MemoryWriter

if TYPE_CHECKING:
    from jaos.memory.providers.sqlite_store import SQLiteStore


class SQLiteTransaction(MemoryTransaction, MemoryWriter):
    """
    Native SQLite transaction for atomic memory write operations.

    The transaction uses the SQLiteStore connection and holds the store lock
    for the complete transaction lifetime.
    """

    def __init__(self, store: SQLiteStore) -> None:
        self._store = store
        self._active = False
        self._completed = False

    def __enter__(self) -> Self:
        """
        Begin a native SQLite transaction.
        """
        if self._active:
            raise RuntimeError("transaction is already active")

        if self._completed:
            raise RuntimeError(
                "completed transaction cannot be reused"
            )

        self._store._start_transaction()
        self._active = True

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """
        Commit successful operations or roll back after an exception.
        """
        if self._completed:
            return False

        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        return False

    def create(self, record: MemoryRecord) -> MemoryRecord:
        """
        Persist a new memory within the active transaction.
        """
        self._require_active()

        return self._store._create_with_connection(
            self._store._connection,
            record,
        )

    def update(self, record: MemoryRecord) -> MemoryRecord:
        """
        Replace an existing memory within the active transaction.
        """
        self._require_active()

        return self._store._update_with_connection(
            self._store._connection,
            record,
        )

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory within the active transaction.
        """
        self._require_active()

        normalized_id = self._store._validate_memory_id(
            memory_id
        )

        return self._store._delete_with_connection(
            self._store._connection,
            normalized_id,
        )

    def clear(self) -> int:
        """
        Delete all memories within the active transaction.
        """
        self._require_active()

        return self._store._clear_with_connection(
            self._store._connection
        )

    def commit(self) -> None:
        """
        Commit every operation in the active transaction.
        """
        self._require_active()

        try:
            self._store._commit_transaction()
        finally:
            self._finish()

    def rollback(self) -> None:
        """
        Roll back every operation in the active transaction.
        """
        self._require_active()

        try:
            self._store._rollback_transaction()
        finally:
            self._finish()

    def _require_active(self) -> None:
        """
        Reject operations outside an active transaction.
        """
        if not self._active:
            raise RuntimeError("transaction is not active")

    def _finish(self) -> None:
        """
        Mark the transaction as completed and non-reusable.
        """
        self._active = False
        self._completed = True