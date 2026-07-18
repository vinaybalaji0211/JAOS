from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import RLock
from time import perf_counter
from typing import TYPE_CHECKING

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult
from jaos.memory.providers.sqlite_schema import (
    create_sqlite_connection,
    initialize_sqlite_schema,
)
from jaos.memory.providers.sqlite_serializer import (
    SQLiteMemorySerializer,
)
from jaos.memory.storage.memory_store import MemoryStore
from jaos.memory.storage.memory_transaction import MemoryTransaction

if TYPE_CHECKING:
    from jaos.memory.providers.sqlite_transaction import (
        SQLiteTransaction,
    )


INSERT_MEMORY = """
INSERT INTO memories (
    memory_id,
    content,
    memory_type,
    memory_scope,
    identity_json,
    source,
    importance,
    confidence,
    lifecycle_state,
    metadata_json,
    statistics_json,
    created_at,
    updated_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""


SELECT_MEMORY_BY_ID = """
SELECT
    memory_id,
    content,
    memory_type,
    memory_scope,
    identity_json,
    source,
    importance,
    confidence,
    lifecycle_state,
    metadata_json,
    statistics_json,
    created_at,
    updated_at
FROM memories
WHERE memory_id = ?;
"""


UPDATE_MEMORY = """
UPDATE memories
SET
    content = ?,
    memory_type = ?,
    memory_scope = ?,
    identity_json = ?,
    source = ?,
    importance = ?,
    confidence = ?,
    lifecycle_state = ?,
    metadata_json = ?,
    statistics_json = ?,
    created_at = ?,
    updated_at = ?
WHERE memory_id = ?;
"""


DELETE_MEMORY = """
DELETE FROM memories
WHERE memory_id = ?;
"""


DELETE_ALL_MEMORIES = """
DELETE FROM memories;
"""


COUNT_ALL_MEMORIES = """
SELECT COUNT(*) AS record_count
FROM memories;
"""


SELECT_ALL_MEMORIES = """
SELECT
    memory_id,
    content,
    memory_type,
    memory_scope,
    identity_json,
    source,
    importance,
    confidence,
    lifecycle_state,
    metadata_json,
    statistics_json,
    created_at,
    updated_at
FROM memories;
"""


class SQLiteStore(MemoryStore):
    """
    Persistent SQLite implementation of the MemoryStore contract.

    SQLite-specific behavior remains encapsulated inside this provider so
    higher JAOS layers depend only on MemoryStore.
    """

    def __init__(
        self,
        database_path: str | Path,
    ) -> None:
        if not isinstance(database_path, (str, Path)):
            raise TypeError(
                "database_path must be a string or pathlib.Path"
            )

        if isinstance(database_path, str) and not database_path.strip():
            raise ValueError(
                "database_path must not be empty"
            )

        self._database_path = database_path
        self._lock = RLock()
        self._connection = create_sqlite_connection(database_path)
        self._closed = False
        self._transaction_active = False

        initialize_sqlite_schema(self._connection)

    @property
    def database_path(self) -> str | Path:
        """
        Return the configured SQLite database path.
        """
        return self._database_path

    @property
    def is_closed(self) -> bool:
        """
        Return whether this store has been closed.
        """
        return self._closed

    def create(self, record: MemoryRecord) -> MemoryRecord:
        """
        Persist a new memory record.
        """
        self._require_open()

        with self._lock:
            self._ensure_direct_write_allowed()
            return self._create_with_connection(
                self._connection,
                record,
            )

    def get(self, memory_id: str) -> MemoryRecord | None:
        """
        Retrieve one memory record by identifier.
        """
        self._require_open()
        normalized_id = self._validate_memory_id(memory_id)

        with self._lock:
            row = self._connection.execute(
                SELECT_MEMORY_BY_ID,
                (normalized_id,),
            ).fetchone()

        if row is None:
            return None

        return SQLiteMemorySerializer.from_row(row)

    def update(self, record: MemoryRecord) -> MemoryRecord:
        """
        Replace an existing memory record.
        """
        self._require_open()

        with self._lock:
            self._ensure_direct_write_allowed()
            return self._update_with_connection(
                self._connection,
                record,
            )

    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Returns True when a record was deleted.
        """
        self._require_open()
        normalized_id = self._validate_memory_id(memory_id)

        with self._lock:
            self._ensure_direct_write_allowed()
            return self._delete_with_connection(
                self._connection,
                normalized_id,
            )

    def search(
        self,
        query: MemoryQuery,
        memory_filter: MemoryFilter | None = None,
    ) -> MemoryResult:
        """
        Search stored memories using case-insensitive substring matching.
        """
        self._require_open()

        if not isinstance(query, MemoryQuery):
            raise TypeError("query must be a MemoryQuery")

        if (
            memory_filter is not None
            and not isinstance(memory_filter, MemoryFilter)
        ):
            raise TypeError(
                "memory_filter must be a MemoryFilter or None"
            )

        started_at = perf_counter()

        sql, parameters = self._build_candidate_query(
            query=query,
            memory_filter=memory_filter,
            require_text_match=True,
        )

        with self._lock:
            rows = self._connection.execute(
                sql,
                parameters,
            ).fetchall()

        matching_records = [
            SQLiteMemorySerializer.from_row(row)
            for row in rows
        ]

        matching_records = [
            record
            for record in matching_records
            if self._matches_query(record, query)
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
        self._require_open()
        self._validate_pagination(limit=limit, offset=offset)

        if (
            memory_filter is not None
            and not isinstance(memory_filter, MemoryFilter)
        ):
            raise TypeError(
                "memory_filter must be a MemoryFilter or None"
            )

        started_at = perf_counter()

        sql, parameters = self._build_candidate_query(
            query=None,
            memory_filter=memory_filter,
            require_text_match=False,
        )

        with self._lock:
            rows = self._connection.execute(
                sql,
                parameters,
            ).fetchall()

        matching_records = [
            SQLiteMemorySerializer.from_row(row)
            for row in rows
        ]

        if memory_filter is not None:
            matching_records = [
                record
                for record in matching_records
                if self._matches_filter(record, memory_filter)
            ]

        matching_records.sort(
            key=lambda record: record.created_at,
            reverse=True,
        )

        total_matches = len(matching_records)
        paginated_records = matching_records[
            offset : offset + limit
        ]
        query_time_ms = (perf_counter() - started_at) * 1000.0

        return MemoryResult(
            records=paginated_records,
            total_matches=total_matches,
            query_time_ms=query_time_ms,
        )

    def count(
        self,
        memory_filter: MemoryFilter | None = None,
    ) -> int:
        """
        Count stored memories matching an optional filter.
        """
        self._require_open()

        if memory_filter is None:
            with self._lock:
                row = self._connection.execute(
                    COUNT_ALL_MEMORIES
                ).fetchone()

            return int(row["record_count"])

        if not isinstance(memory_filter, MemoryFilter):
            raise TypeError(
                "memory_filter must be a MemoryFilter or None"
            )

        result = self.list_records(
            memory_filter=memory_filter,
            limit=1,
            offset=0,
        )

        return result.total_matches

    def clear(self) -> int:
        """
        Delete all stored memories.

        Returns the number of deleted records.
        """
        self._require_open()

        with self._lock:
            self._ensure_direct_write_allowed()
            return self._clear_with_connection(self._connection)

    def begin_transaction(self) -> MemoryTransaction:
        """
        Create a new SQLite transaction.
        """
        self._require_open()

        from jaos.memory.providers.sqlite_transaction import (
            SQLiteTransaction,
        )

        return SQLiteTransaction(self)

    def close(self) -> None:
        """
        Close the SQLite connection.

        Closing an already closed store has no effect.
        """
        with self._lock:
            if self._closed:
                return

            if self._transaction_active:
                raise RuntimeError(
                    "cannot close SQLiteStore during an active transaction"
                )

            self._connection.close()
            self._closed = True

    def __enter__(self) -> SQLiteStore:
        """
        Enter the store context.
        """
        self._require_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool:
        """
        Close the store when leaving its context.
        """
        self.close()
        return False

    def _create_with_connection(
        self,
        connection: sqlite3.Connection,
        record: MemoryRecord,
    ) -> MemoryRecord:
        """
        Create a record using the supplied SQLite connection.
        """
        if not isinstance(record, MemoryRecord):
            raise TypeError("record must be a MemoryRecord")

        try:
            connection.execute(
                INSERT_MEMORY,
                SQLiteMemorySerializer.to_parameters(record),
            )
        except sqlite3.IntegrityError as error:
            raise ValueError(
                f"Memory record already exists: {record.memory_id}"
            ) from error

        return record

    def _update_with_connection(
        self,
        connection: sqlite3.Connection,
        record: MemoryRecord,
    ) -> MemoryRecord:
        """
        Update a record using the supplied SQLite connection.
        """
        if not isinstance(record, MemoryRecord):
            raise TypeError("record must be a MemoryRecord")

        parameters = SQLiteMemorySerializer.to_parameters(record)

        update_parameters = (
            parameters[1],
            parameters[2],
            parameters[3],
            parameters[4],
            parameters[5],
            parameters[6],
            parameters[7],
            parameters[8],
            parameters[9],
            parameters[10],
            parameters[11],
            parameters[12],
            record.memory_id,
        )

        cursor = connection.execute(
            UPDATE_MEMORY,
            update_parameters,
        )

        if cursor.rowcount == 0:
            raise ValueError(
                f"Memory record does not exist: {record.memory_id}"
            )

        return record

    def _delete_with_connection(
        self,
        connection: sqlite3.Connection,
        memory_id: str,
    ) -> bool:
        """
        Delete a record using the supplied SQLite connection.
        """
        cursor = connection.execute(
            DELETE_MEMORY,
            (memory_id,),
        )

        return cursor.rowcount > 0

    def _clear_with_connection(
        self,
        connection: sqlite3.Connection,
    ) -> int:
        """
        Delete every record using the supplied SQLite connection.
        """
        row = connection.execute(
            COUNT_ALL_MEMORIES
        ).fetchone()

        deleted_count = int(row["record_count"])
        connection.execute(DELETE_ALL_MEMORIES)

        return deleted_count

    def _start_transaction(self) -> None:
        """
        Acquire the store for a native SQLite transaction.
        """
        self._require_open()
        self._lock.acquire()

        try:
            if self._transaction_active:
                raise RuntimeError(
                    "a SQLite transaction is already active"
                )

            self._connection.execute("BEGIN IMMEDIATE")
            self._transaction_active = True
        except BaseException:
            self._lock.release()
            raise

    def _commit_transaction(self) -> None:
        """
        Commit the active native SQLite transaction.
        """
        if not self._transaction_active:
            raise RuntimeError("transaction is not active")

        try:
            self._connection.commit()
        finally:
            self._transaction_active = False
            self._lock.release()

    def _rollback_transaction(self) -> None:
        """
        Roll back the active native SQLite transaction.
        """
        if not self._transaction_active:
            raise RuntimeError("transaction is not active")

        try:
            self._connection.rollback()
        finally:
            self._transaction_active = False
            self._lock.release()

    def _ensure_direct_write_allowed(self) -> None:
        """
        Reject direct writes while a transaction owns the store.
        """
        if self._transaction_active:
            raise RuntimeError(
                "direct writes are unavailable during an active transaction"
            )

    def _require_open(self) -> None:
        """
        Reject operations after the provider has been closed.
        """
        if self._closed:
            raise RuntimeError("SQLiteStore is closed")

    @staticmethod
    def _validate_memory_id(memory_id: str) -> str:
        """
        Validate and normalize a memory identifier.
        """
        if not isinstance(memory_id, str):
            raise TypeError("memory_id must be a string")

        normalized_id = memory_id.strip()

        if not normalized_id:
            raise ValueError(
                "memory_id must be a non-empty string"
            )

        return normalized_id

    @staticmethod
    def _validate_pagination(
        *,
        limit: int,
        offset: int,
    ) -> None:
        """
        Validate pagination values.
        """
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero"
            )

        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")

        if offset < 0:
            raise ValueError(
                "offset cannot be negative"
            )

    @classmethod
    def _build_candidate_query(
        cls,
        *,
        query: MemoryQuery | None,
        memory_filter: MemoryFilter | None,
        require_text_match: bool,
    ) -> tuple[str, tuple[object, ...]]:
        """
        Build a parameterized SQL query for indexed candidate selection.

        Identity and tag checks are completed after deserialization to preserve
        exact parity with InMemoryStore.
        """
        conditions: list[str] = []
        parameters: list[object] = []

        if require_text_match:
            if query is None:
                raise ValueError(
                    "query is required for text matching"
                )

            conditions.append(
                "instr(lower(content), lower(?)) > 0"
            )
            parameters.append(query.query_text)

        if query is not None:
            if query.memory_types:
                placeholders = ", ".join(
                    "?" for _ in query.memory_types
                )
                conditions.append(
                    f"memory_type IN ({placeholders})"
                )
                parameters.extend(
                    memory_type.value
                    for memory_type in query.memory_types
                )

            if query.scope is not None:
                conditions.append("memory_scope = ?")
                parameters.append(query.scope.value)

            conditions.append("importance >= ?")
            parameters.append(query.minimum_importance)

            conditions.append("confidence >= ?")
            parameters.append(query.minimum_confidence)

        if memory_filter is not None:
            if memory_filter.memory_type is not None:
                conditions.append("memory_type = ?")
                parameters.append(
                    memory_filter.memory_type.value
                )

            if memory_filter.memory_scope is not None:
                conditions.append("memory_scope = ?")
                parameters.append(
                    memory_filter.memory_scope.value
                )

            conditions.append("importance >= ?")
            parameters.append(
                memory_filter.minimum_importance
            )

        sql = SELECT_ALL_MEMORIES.strip().rstrip(";")

        if conditions:
            sql += "\nWHERE " + "\nAND ".join(conditions)

        sql += ";"

        return sql, tuple(parameters)

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
            and record.identity.scope
            != memory_filter.memory_scope
        ):
            return False

        if (
            record.importance
            < memory_filter.minimum_importance
        ):
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

            if not set(memory_filter.tags).issubset(
                record_tags
            ):
                return False

        return True