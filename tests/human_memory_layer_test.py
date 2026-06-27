from brain.human_memory_layer import (
    HumanMemoryLayer
)

memory = HumanMemoryLayer()

memory.remember(
    "Vinay",
    "preferences",
    "Step-by-step instructions"
)

memory.remember(
    "Vinay",
    "projects",
    "JARVIS OS"
)

memory.remember(
    "Vinay",
    "projects",
    "Underwater Object Detection"
)

memory.remember(
    "Vinay",
    "habits",
    "Works on AI projects daily"
)

memory.show_person(
    "Vinay"
)