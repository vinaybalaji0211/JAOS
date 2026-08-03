from brain.cloud_memory_architecture import CloudMemoryArchitecture

memory = (
    CloudMemoryArchitecture()
)

memory.store(
    "user_name",
    "Vinay"
)

memory.store(
    "project",
    "JARVIS"
)

memory.store(
    "goal",
    "Autonomous AI Assistant"
)

memory.show_memory()