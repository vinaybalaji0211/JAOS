from brain.agent_learning_manager import (
    AgentLearningManager
)

manager = AgentLearningManager()

manager.register_agent(
    "Research Agent"
)

manager.record_lesson(
    "Research Agent",
    "Fact-checked sources improve accuracy."
)

manager.record_lesson(
    "Research Agent",
    "Multiple source validation reduces errors."
)

manager.show_learning(
    "Research Agent"
)