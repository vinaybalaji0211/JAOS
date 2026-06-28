"""
JAOS Component: MemoryRegistry

Purpose:
    Store and manage WorkingMemory objects.

Responsibilities:
    - Store memory
    - Retrieve memory
    - Update memory
    - Remove memory
    - List memory

Non-Responsibilities:
    - AI reasoning
    - Long-term storage
    - Memory ranking
"""

from executive_brain.memory.working_memory import WorkingMemory
from executive_brain.registries.base_registry import BaseRegistry


class MemoryRegistry(BaseRegistry):
    """Registry responsible for storing WorkingMemory objects."""

    def __init__(self):
        super().__init__()

    def add_memory(self, memory: WorkingMemory):
        if not isinstance(memory, WorkingMemory):
            raise TypeError(
                "memory must be an instance of WorkingMemory."
            )

        self.add("working_memory", memory)

    def get_memory(self):
        return self.get("working_memory")

    def update_memory(self, memory: WorkingMemory):
        if not isinstance(memory, WorkingMemory):
            raise TypeError(
                "memory must be an instance of WorkingMemory."
            )

        self.update("working_memory", memory)

    def remove_memory(self):
        return self.remove("working_memory")

    def has_memory(self):
        return self.get("working_memory") is not None