from brain.dynamic_agent_assignment_engine import DynamicAgentAssignmentEngine

DynamicAgentAssignmentEngine.show_assignments(
    "Gemini",
    [
        "vision",
        "research",
        "conversation"
    ]
)

DynamicAgentAssignmentEngine.show_assignments(
    "DeepSeek",
    [
        "coding",
        "debugging",
        "reasoning"
    ]
)

DynamicAgentAssignmentEngine.show_assignments(
    "Unknown AI",
    [
        "music"
    ]
)