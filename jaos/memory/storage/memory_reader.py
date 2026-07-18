from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_record import MemoryRecord
from jaos.memory.models.memory_result import MemoryResult


class MemoryReader(ABC):
    """
    Read-only contract for retrieving stored memories.
    """

    @abstractmethod
    def get(self, memory_id: str) -> MemoryRecord | None:
        """
        Retrieve one memory record by its identifier.
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