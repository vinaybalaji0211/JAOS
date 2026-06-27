from brain.master_brain_agent import (
    MasterBrainAgent
)

brain = MasterBrainAgent()

brain.register_agent(
    "Memory Agent"
)

brain.register_agent(
    "Security Agent"
)

brain.register_agent(
    "Research Agent"
)

brain.receive_request(
    "Analyze system security"
)

brain.show_status()