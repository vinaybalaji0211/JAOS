from memory.memory_manager import MemoryManager

manager = MemoryManager()

manager.remember_short_term(
    "User is currently working on Phase 3 Step 3"
)

manager.remember_long_term(
    "Memory Manager system was created in Phase 3 Step 3"
)

manager.show_all()