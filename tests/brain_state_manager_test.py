from brain.brain_state_manager import BrainStateManager

brain = BrainStateManager()

brain.show_state()

brain.set_state(
    "UNDERSTANDING"
)

brain.show_state()

brain.set_state(
    "PLANNING"
)

brain.show_state()

brain.set_state(
    "REASONING"
)

brain.show_state()

brain.set_state(
    "EXECUTING"
)

brain.show_state()