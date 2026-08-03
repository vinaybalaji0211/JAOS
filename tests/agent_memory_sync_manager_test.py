from brain.agent_memory_sync_manager import AgentMemorySyncManager

manager = (
    AgentMemorySyncManager()
)

manager.sync_agent(
    "ResearchAgent",
    "Quantum Physics Knowledge"
)

manager.sync_agent(
    "MemoryAgent",
    "Evolution Memory"
)

manager.sync_agent(
    "SecurityAgent",
    "Threat Database"
)

manager.show_sync_log()