from __future__ import annotations

from abc import ABC, abstractmethod

from jaos.memory.models.memory_record import MemoryRecord


class MemoryWriter(ABC):
    """
    Write-only contract for modifying stored memories.
    """

    @abstractmethod
    def create(self, record: MemoryRecord) -> MemoryRecord:
        """
        Persist a new memory record.
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
    def clear(self) -> int:
        """
        Delete all stored memories.

        Returns the number of deleted records.
        """