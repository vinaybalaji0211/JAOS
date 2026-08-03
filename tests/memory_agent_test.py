from brain.memory_agent import MemoryAgent

agent = MemoryAgent()

agent.store_memory(
    "Security Threat Response Engine is roadmap locked",
    "SECURITY",
    "HIGH"
)

agent.store_memory(
    "Cloud Memory Architecture planned",
    "MEMORY",
    "HIGH"
)

agent.store_memory(
    "Phase 16 Multi-Agent System active",
    "SYSTEM",
    "NORMAL"
)

agent.show_memories()

print(
    "\nSearch Results:\n"
)

results = agent.search_memory(
    "cloud"
)

for item in results:

    print(item)