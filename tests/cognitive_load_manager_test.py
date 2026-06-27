from brain.cognitive_load_manager import (
    CognitiveLoadManager
)


CognitiveLoadManager.show_load(
    active_tasks=2,
    active_agents=1,
    priority_pressure=10,
    system_load=20
)

CognitiveLoadManager.show_load(
    active_tasks=5,
    active_agents=3,
    priority_pressure=30,
    system_load=40
)