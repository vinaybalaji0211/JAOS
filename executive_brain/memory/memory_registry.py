from executive_brain.memory.working_memory import WorkingMemory
from executive_brain.registries.base_registry import BaseRegistry


class MemoryRegistry(BaseRegistry):
    def __init__(self):
        super().__init__()

    def add_memory(self, memory: WorkingMemory):
        if not isinstance(memory, WorkingMemory):
            raise TypeError("memory must be an instance of WorkingMemory.")

        self.add("working_memory", memory)

    def get_memory(self):
        return self.get("working_memory")

    def update_memory(self, memory: WorkingMemory):
        if not isinstance(memory, WorkingMemory):
            raise TypeError("memory must be an instance of WorkingMemory.")

        self.update("working_memory", memory)

    def remove_memory(self):
        return self.remove("working_memory")

    def has_memory(self):
        return self.get("working_memory") is not None