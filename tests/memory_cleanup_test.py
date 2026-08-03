from memory.long_term_memory import LongTermMemory
from memory.memory_cleanup import MemoryCleanup

LongTermMemory.add(
    "User opened VS Code"
)

LongTermMemory.add(
    "Critical Phase 3 memory goal completed"
)

MemoryCleanup.show_cleanup(
    min_score=3
)

LongTermMemory.show()