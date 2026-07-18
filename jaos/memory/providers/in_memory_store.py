from __future__ import annotations

from threading import RLock
from time import perf_counter

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult
from jaos.memory.storage.memory_store import MemoryStore
from jaos.memory.providers.in_memory_transaction import (
    InMemoryTransaction,
)
from jaos.memory.storage.memory_transaction import MemoryTransaction


class InMemoryStore(MemoryStore):
    """
    Thread-safe in-memory implementation of the MemoryStore contract.
    """

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}
        self._lock = RLock()

    def create(self, record: MemoryRecord) -> MemoryRecord:
        """
        Persist a new memory record.
        """
        memory_id = record.memory_id

        with self._lock:
            if memory_id in self._records:
                raise ValueError(
                    f"Memory record already exists: {memory_id}"
                )

            self._records[memory_id] = record
            return record

    def get(self, memory_id: str) -> MemoryRecord | None:
        """
        Retrieve one memory record by its identifier.
        """
        with self._lock:
            return self._records.get(memory_id)

    def update(self, record: MemoryRecord) -> MemoryRecord:
        """
        Replace an existing memory record.
        """
        memory_id = record.memory_id

        with self._lock:
            if memory_id not in self._records:
                raise ValueError(
                    f"Memory record does not exist: {memory_id}"
                )

            self._records[memory_id] = record
            return record

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Returns True when a record was deleted.
        """
        with self._lock:
            if memory_id not in self._records:
                return False

            del self._records[memory_id]
            return True

    def search(
        self,
        query: MemoryQuery,
        memory_filter: MemoryFilter | None = None,
    ) -> MemoryResult:
        """
        Search stored memories using a query and optional filters.

        Search is currently implemented as case-insensitive text matching.
        """
        started_at = perf_counter()
        normalized_query = query.query_text.casefold()

        with self._lock:
            matching_records = [
                record
                for record in self._records.values()
                if normalized_query in record.content.casefold()
                and self._matches_query(record, query)
                and (
                    memory_filter is None
                    or self._matches_filter(record, memory_filter)
                )
            ]

        matching_records.sort(
            key=lambda record: (
                record.importance,
                record.confidence,
                record.updated_at,
            ),
            reverse=True,
        )

        total_matches = len(matching_records)
        limited_records = matching_records[:query.max_results]
        query_time_ms = (perf_counter() - started_at) * 1000.0

        return MemoryResult(
            records=limited_records,
            total_matches=total_matches,
            query_time_ms=query_time_ms,
        )

    def list_records(
        self,
        memory_filter: MemoryFilter | None = None,
        *,
        limit: int = 100,
        offset: int = 0,
    ) -> MemoryResult:
        """
        Return stored memories using optional filtering and pagination.
        """
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")

        if limit <= 0:
            raise ValueError("limit must be greater than zero")

        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")

        if offset < 0:
            raise ValueError("offset cannot be negative")

        started_at = perf_counter()

        with self._lock:
            if memory_filter is None:
                matching_records = list(self._records.values())
            else:
                matching_records = [
                    record
                    for record in self._records.values()
                    if self._matches_filter(record, memory_filter)
                ]

        matching_records.sort(
            key=lambda record: record.created_at,
            reverse=True,
        )

        total_matches = len(matching_records)
        paginated_records = matching_records[offset : offset + limit]
        query_time_ms = (perf_counter() - started_at) * 1000.0

        return MemoryResult(
            records=paginated_records,
            total_matches=total_matches,
            query_time_ms=query_time_ms,
        )

    def count(self, memory_filter: MemoryFilter | None = None) -> int:
        """
        Count stored memories matching an optional filter.
        """
        with self._lock:
            if memory_filter is None:
                return len(self._records)

            return sum(
                1
                for record in self._records.values()
                if self._matches_filter(record, memory_filter)
            )

    def clear(self) -> int:
        """
        Delete all stored memories.

        Returns the number of deleted records.
        """
        with self._lock:
            deleted_count = len(self._records)
            self._records.clear()
            return deleted_count
    def begin_transaction(self) -> MemoryTransaction:
        """
        Create a new isolated transaction for this store.
        """
        return InMemoryTransaction(self)

    @staticmethod
    def _matches_query(
        record: MemoryRecord,
        query: MemoryQuery,
    ) -> bool:
        """
        Return True when a record satisfies all query criteria.
        """
        if (
            query.memory_types
            and record.memory_type not in query.memory_types
        ):
            return False

        if (
            query.scope is not None
            and record.identity.scope != query.scope
        ):
            return False

        if (
            query.identity is not None
            and record.identity != query.identity
        ):
            return False

        if record.importance < query.minimum_importance:
            return False

        if record.confidence < query.minimum_confidence:
            return False

        return True

    @staticmethod
    def _matches_filter(
        record: MemoryRecord,
        memory_filter: MemoryFilter,
    ) -> bool:
        """
        Return True when a record satisfies all filter conditions.
        """
        if (
            memory_filter.memory_type is not None
            and record.memory_type != memory_filter.memory_type
        ):
            return False

        if (
            memory_filter.memory_scope is not None
            and record.identity.scope != memory_filter.memory_scope
        ):
            return False

        if record.importance < memory_filter.minimum_importance:
            return False

        if memory_filter.tags:
            metadata_tags = record.metadata.get("tags", ())

            if isinstance(metadata_tags, str):
                record_tags = {metadata_tags}
            else:
                try:
                    record_tags = set(metadata_tags)
                except TypeError:
                    return False

            if not set(memory_filter.tags).issubset(record_tags):
                return False

        return True