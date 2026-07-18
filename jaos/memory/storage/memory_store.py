from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult


class MemoryStore(ABC):
    """
    Provider-independent contract for persistent memory storage.
    """

    @abstractmethod
    def create(self, record: MemoryRecord) -> MemoryRecord:
        """
        Persist a new memory record.
        """

    @abstractmethod
    def get(self, memory_id: str) -> MemoryRecord | None:
        """
        Retrieve one memory record by its identifier.
        """

    @abstractmethod
    def update(self, record: MemoryRecord) -> MemoryRecord:
        """
        Replace an existing memory record.
        """

    @abstractmethod
    def delete(self, memory_id: str) -> bool:
        """
        Delete a memory record.

        Returns True when a record was deleted.
        """

    @abstractmethod
    def search(
        self,
        query: MemoryQuery,
        memory_filter: MemoryFilter | None = None,
    ) -> MemoryResult:
        """
        Search stored memories using a query and optional filters.
        """

    @abstractmethod
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

    @abstractmethod
    def count(self, memory_filter: MemoryFilter | None = None) -> int:
        """
        Count stored memories matching an optional filter.
        """

    @abstractmethod
    def clear(self) -> int:
        """
        Delete all stored memories.

        Returns the number of deleted records.
        """