from brain.memory_consolidation import MemoryConsolidation


memory = MemoryConsolidation()

memory.add_short_term(
    "User prefers step-by-step JARVIS building",
    important=True
)

memory.add_short_term(
    "Temporary terminal output",
    important=False
)

memory.show_memory()

memory.consolidate()

memory.show_memory()