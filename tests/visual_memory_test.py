from brain.visual_memory import (
    VisualMemory
)

memory = VisualMemory()

memory.remember(
    "screen_text",
    "ModuleNotFoundError detected"
)

memory.remember(
    "camera_frame",
    "sample_frame_001"
)

memory.remember(
    "gui_state",
    "VS Code terminal open"
)

memory.show_memories()