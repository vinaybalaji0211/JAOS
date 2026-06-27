from brain.agent_communication_bus import (
    AgentCommunicationBus
)

bus = AgentCommunicationBus()

bus.send_message(
    "ResearchAgent",
    "SecurityAgent",
    "Found API vulnerability."
)

bus.send_message(
    "MemoryAgent",
    "ExecutiveBrain",
    "Knowledge updated."
)

bus.show_messages()

print(
    bus.get_messages_for(
        "SecurityAgent"
    )
)