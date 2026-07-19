from __future__ import annotations

from threading import RLock
from time import perf_counter
from typing import TYPE_CHECKING, Any

from psycopg import Connection
from psycopg.errors import UniqueViolation
from psycopg.rows import dict_row

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult
from jaos.memory.providers.postgres_schema import (
    create_postgres_connection,
    initialize_postgres_schema,
)
from jaos.memory.providers.postgres_serializer import (
    PostgreSQLMemorySerializer,
)
from jaos.memory.storage.memory_store import MemoryStore
from jaos.memory.storage.memory_transaction import MemoryTransaction

if TYPE_CHECKING:
    from jaos.memory.providers.postgres_transaction import (
        PostgreSQLTransaction,
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
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s::jsonb,
    %s,
    %s,
    %s,
    %s,
    %s::jsonb,
    %s::jsonb,
    %s::timestamptz,
    %s::timestamptz
);
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
WHERE memory_id = %s;
"""

UPDATE_MEMORY = """
UPDATE memories
SET
    content = %s,
    memory_type = %s,
    memory_scope = %s,
    identity_json = %s::jsonb,
    source = %s,
    importance = %s,
    confidence = %s,
    lifecycle_state = %s,
    metadata_json = %s::jsonb,
    statistics_json = %s::jsonb,
    created_at = %s::timestamptz,
    updated_at = %s::timestamptz
WHERE memory_id = %s;
"""

DELETE_MEMORY = """
DELETE FROM memories
WHERE memory_id = %s;
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


class PostgreSQLStore(MemoryStore):
    """Persistent PostgreSQL implementation of the MemoryStore contract."""

    def __init__(self, connection_string: str) -> None:
        if not isinstance(connection_string, str):
            raise TypeError("connection_string must be a string")

        normalized_connection_string = connection_string.strip()
        if not normalized_connection_string:
            raise ValueError("connection_string must not be empty")

        self._connection_string = normalized_connection_string
        self._lock = RLock()
        self._connection = create_postgres_connection(
            normalized_connection_string
        )
        self._closed = False
        self._transaction_active = False

        initialize_postgres_schema(self._connection)

    @property
    def connection_string(self) -> str:
        return self._connection_string

    @property
    def is_closed(self) -> bool:
        return self._closed

    def create(self, record: MemoryRecord) -> MemoryRecord:
        self._require_open()
        with self._lock:
            self._ensure_direct_write_allowed()
            result = self._create_with_connection(self._connection, record)
            self._connection.commit()
            return result

    def get(self, memory_id: str) -> MemoryRecord | None:
        self._require_open()
        normalized_id = self._validate_memory_id(memory_id)

        with self._lock:
            with self._connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(SELECT_MEMORY_BY_ID, (normalized_id,))
                row = cursor.fetchone()

        if row is None:
            return None

        return PostgreSQLMemorySerializer.from_row(row)

    def update(self, record: MemoryRecord) -> MemoryRecord:
        self._require_open()
        with self._lock:
            self._ensure_direct_write_allowed()
            result = self._update_with_connection(self._connection, record)
            self._connection.commit()
            return result

    def delete(self, memory_id: str) -> bool:
        self._require_open()
        normalized_id = self._validate_memory_id(memory_id)

        with self._lock:
            self._ensure_direct_write_allowed()
            deleted = self._delete_with_connection(
                self._connection,
                normalized_id,
            )
            self._connection.commit()
            return deleted

    def search(
        self,
        query: MemoryQuery,
        memory_filter: MemoryFilter | None = None,
    ) -> MemoryResult:
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
            with self._connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(sql, parameters)
                rows = cursor.fetchall()

        matching_records = [
            PostgreSQLMemorySerializer.from_row(row)
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
            with self._connection.cursor(row_factory=dict_row) as cursor:
                cursor.execute(sql, parameters)
                rows = cursor.fetchall()

        matching_records = [
            PostgreSQLMemorySerializer.from_row(row)
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
        paginated_records = matching_records[offset : offset + limit]
        query_time_ms = (perf_counter() - started_at) * 1000.0

        return MemoryResult(
            records=paginated_records,
            total_matches=total_matches,
            query_time_ms=query_time_ms,
        )

    def count(self, memory_filter: MemoryFilter | None = None) -> int:
        self._require_open()

        if memory_filter is None:
            with self._lock:
                with self._connection.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(COUNT_ALL_MEMORIES)
                    row = cursor.fetchone()

            if row is None:
                return 0

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
        self._require_open()
        with self._lock:
            self._ensure_direct_write_allowed()
            deleted_count = self._clear_with_connection(self._connection)
            self._connection.commit()
            return deleted_count

    def begin_transaction(self) -> MemoryTransaction:
        self._require_open()
        from jaos.memory.providers.postgres_transaction import (
            PostgreSQLTransaction,
        )
        return PostgreSQLTransaction(self)

    def close(self) -> None:
        with self._lock:
            if self._closed:
                return
            if self._transaction_active:
                raise RuntimeError(
                    "cannot close PostgreSQLStore during an active transaction"
                )
            self._connection.close()
            self._closed = True

    def __enter__(self) -> PostgreSQLStore:
        self._require_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> bool:
        self.close()
        return False

    def _create_with_connection(
        self,
        connection: Connection[Any],
        record: MemoryRecord,
    ) -> MemoryRecord:
        if not isinstance(record, MemoryRecord):
            raise TypeError("record must be a MemoryRecord")

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    INSERT_MEMORY,
                    PostgreSQLMemorySerializer.to_parameters(record),
                )
        except UniqueViolation as error:
            raise ValueError(
                f"Memory record already exists: {record.memory_id}"
            ) from error

        return record

    def _update_with_connection(
        self,
        connection: Connection[Any],
        record: MemoryRecord,
    ) -> MemoryRecord:
        if not isinstance(record, MemoryRecord):
            raise TypeError("record must be a MemoryRecord")

        parameters = PostgreSQLMemorySerializer.to_parameters(record)
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

        with connection.cursor() as cursor:
            cursor.execute(UPDATE_MEMORY, update_parameters)
            if cursor.rowcount == 0:
                raise ValueError(
                    f"Memory record does not exist: {record.memory_id}"
                )

        return record

    def _delete_with_connection(
        self,
        connection: Connection[Any],
        memory_id: str,
    ) -> bool:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_MEMORY, (memory_id,))
            return cursor.rowcount > 0

    def _clear_with_connection(
        self,
        connection: Connection[Any],
    ) -> int:
        with connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(COUNT_ALL_MEMORIES)
            row = cursor.fetchone()
            deleted_count = int(row["record_count"]) if row else 0
            cursor.execute(DELETE_ALL_MEMORIES)

        return deleted_count

    def _start_transaction(self) -> None:
        self._require_open()
        self._lock.acquire()

        try:
            if self._transaction_active:
                raise RuntimeError(
                    "a PostgreSQL transaction is already active"
                )

            self._connection.execute("BEGIN")
            self._transaction_active = True
        except BaseException:
            self._lock.release()
            raise

    def _commit_transaction(self) -> None:
        if not self._transaction_active:
            raise RuntimeError("transaction is not active")

        try:
            self._connection.commit()
        finally:
            self._transaction_active = False
            self._lock.release()

    def _rollback_transaction(self) -> None:
        if not self._transaction_active:
            raise RuntimeError("transaction is not active")

        try:
            self._connection.rollback()
        finally:
            self._transaction_active = False
            self._lock.release()

    def _ensure_direct_write_allowed(self) -> None:
        if self._transaction_active:
            raise RuntimeError(
                "direct writes are unavailable during an active transaction"
            )

    def _require_open(self) -> None:
        if self._closed:
            raise RuntimeError("PostgreSQLStore is closed")

    @staticmethod
    def _validate_memory_id(memory_id: str) -> str:
        if not isinstance(memory_id, str):
            raise TypeError("memory_id must be a string")

        normalized_id = memory_id.strip()
        if not normalized_id:
            raise ValueError("memory_id must be a non-empty string")

        return normalized_id

    @staticmethod
    def _validate_pagination(*, limit: int, offset: int) -> None:
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        if limit <= 0:
            raise ValueError("limit must be greater than zero")
        if not isinstance(offset, int):
            raise TypeError("offset must be an integer")
        if offset < 0:
            raise ValueError("offset cannot be negative")

    @classmethod
    def _build_candidate_query(
        cls,
        *,
        query: MemoryQuery | None,
        memory_filter: MemoryFilter | None,
        require_text_match: bool,
    ) -> tuple[str, tuple[object, ...]]:
        conditions: list[str] = []
        parameters: list[object] = []

        if require_text_match:
            if query is None:
                raise ValueError("query is required for text matching")
            conditions.append(
                "POSITION(LOWER(%s) IN LOWER(content)) > 0"
            )
            parameters.append(query.query_text)

        if query is not None:
            if query.memory_types:
                placeholders = ", ".join(
                    "%s" for _ in query.memory_types
                )
                conditions.append(
                    f"memory_type IN ({placeholders})"
                )
                parameters.extend(
                    memory_type.value
                    for memory_type in query.memory_types
                )

            if query.scope is not None:
                conditions.append("memory_scope = %s")
                parameters.append(query.scope.value)

            conditions.append("importance >= %s")
            parameters.append(query.minimum_importance)
            conditions.append("confidence >= %s")
            parameters.append(query.minimum_confidence)

        if memory_filter is not None:
            if memory_filter.memory_type is not None:
                conditions.append("memory_type = %s")
                parameters.append(memory_filter.memory_type.value)

            if memory_filter.memory_scope is not None:
                conditions.append("memory_scope = %s")
                parameters.append(memory_filter.memory_scope.value)

            conditions.append("importance >= %s")
            parameters.append(memory_filter.minimum_importance)

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