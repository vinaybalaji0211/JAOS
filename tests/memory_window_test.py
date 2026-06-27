from core.memory_window import MemoryWindow

memory = MemoryWindow(
limit=3
)

memory.add_memory(
"User said hello"
)

memory.add_memory(
"JARVIS replied"
)

memory.add_memory(
"User asked for scheduler"
)

memory.add_memory(
"Oldest memory should be removed"
)

memory.show_memories()