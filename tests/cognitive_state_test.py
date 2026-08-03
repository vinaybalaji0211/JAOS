from brain.cognitive_state import CognitiveState

state = CognitiveState()

state.update(
    "current_task",
    "Phase 5 World Model"
)

state.update(
    "confidence",
    95
)

state.update(
    "time_period",
    "EVENING"
)

state.show_state()