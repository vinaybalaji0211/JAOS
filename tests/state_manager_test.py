from core.state_manager import StateManager


state = StateManager()

state.show_state()

state.set_state(
    "PROCESSING"
)

state.show_state()

state.set_state(
    "IDLE"
)

state.show_state()