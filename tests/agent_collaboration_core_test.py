from brain.agent_collaboration_core import (
    AgentCollaborationCore
)

core = AgentCollaborationCore()

core.start_collaboration(
    "Analyze research paper security risks",
    [
        "ResearchAgent",
        "DocumentAgent",
        "SecurityAgent"
    ]
)

core.complete_collaboration(
    "Analyze research paper security risks"
)

core.show_collaborations()