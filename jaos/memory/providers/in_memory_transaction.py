from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Self

from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.storage.memory_transaction import MemoryTransaction
from jaos.memory.storage.memory_writer import MemoryWriter

if TYPE_CHECKING:
    from jaos.memory.providers.in_memory_store import InMemoryStore


class InMemoryTransaction(MemoryTransaction, MemoryWriter):
    """
    Atomic transaction for an InMemoryStore.

    The transaction acquires the store lock, creates an isolated working
    snapshot, and applies the snapshot to the store only when committed.
    """

    def __init__(self, store: InMemoryStore) -> None:
        self._store = store
        self._working_records: dict[str, MemoryRecord] | None = None
        self._active = False
        self._completed = False

    def __enter__(self) -> Self:
        """
        Enter the transaction and create an isolated store snapshot.
        """
        if self._active:
            raise RuntimeError("transaction is already active")

        if self._completed:
            raise RuntimeError("completed transaction cannot be reused")

        self._store._lock.acquire()

        try:
            self._working_records = dict(self._store._records)
            self._active = True
            return self
        except BaseException:
            self._store._lock.release()
            raise

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        """
        Commit successful operations or roll back when an exception occurs.
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
        Add a new record to the transaction snapshot.
        """
        records = self._require_active()
        memory_id = record.memory_id

        if memory_id in records:
            raise ValueError(
                f"Memory record already exists: {memory_id}"
            )

        records[memory_id] = record
        return record

    def update(self, record: MemoryRecord) -> MemoryRecord:
        """
        Replace an existing record in the transaction snapshot.
        """
        records = self._require_active()
        memory_id = record.memory_id

        if memory_id not in records:
            raise ValueError(
                f"Memory record does not exist: {memory_id}"
            )

        records[memory_id] = record
        return record

    def delete(self, memory_id: str) -> bool:
        """
        Delete a record from the transaction snapshot.
        """
        records = self._require_active()

        if memory_id not in records:
            return False

        del records[memory_id]
        return True

    def clear(self) -> int:
        """
        Remove every record from the transaction snapshot.
        """
        records = self._require_active()
        deleted_count = len(records)
        records.clear()
        return deleted_count

    def commit(self) -> None:
        """
        Atomically replace the store state with the transaction snapshot.
        """
        records = self._require_active()

        try:
            self._store._records = dict(records)
        finally:
            self._finish()

    def rollback(self) -> None:
        """
        Discard every pending transaction operation.
        """
        self._require_active()
        self._finish()

    def _require_active(self) -> dict[str, MemoryRecord]:
        """
        Return the working snapshot or reject inactive transactions.
        """
        if not self._active or self._working_records is None:
            raise RuntimeError("transaction is not active")

        return self._working_records

    def _finish(self) -> None:
        """
        Finalize the transaction and release the store lock.
        """
        self._working_records = None
        self._active = False
        self._completed = True
        self._store._lock.release()