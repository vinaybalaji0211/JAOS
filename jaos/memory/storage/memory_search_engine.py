from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.models.memory_filter import MemoryFilter
from jaos.memory.models.memory_query import MemoryQuery
from jaos.memory.models.memory_result import MemoryResult


class MemorySearchEngine(ABC):
    """
    Contract for searching memories.
    """

    @abstractmethod
    def search(
        self,
        query: MemoryQuery,
        memory_filter: MemoryFilter | None = None,
    ) -> MemoryResult:
        """
        Execute a memory search.
        """