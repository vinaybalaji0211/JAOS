from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.models.memory_record import MemoryRecord


class MemoryIndex(ABC):
    """
    Contract for indexing memory records for efficient retrieval.
    """

    @abstractmethod
    def add(self, record: MemoryRecord) -> None:
        """
        Add or refresh a memory record in the index.
        """

    @abstractmethod
    def remove(self, memory_id: str) -> bool:
        """
        Remove a memory record from the index.

        Returns True when an indexed record was removed.
        """

    @abstractmethod
    def rebuild(self, records: list[MemoryRecord]) -> int:
        """
        Rebuild the index from the provided records.

        Returns the number of indexed records.
        """

    @abstractmethod
    def clear(self) -> int:
        """
        Remove all entries from the index.

        Returns the number of removed entries.
        """