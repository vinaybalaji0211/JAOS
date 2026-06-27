from brain.curiosity_engine import (
    CuriosityEngine
)

engine = CuriosityEngine()

engine.add_item(
    "Threat Monitoring",
    "Knowledge gap detected"
)

engine.add_item(
    "Long-Term Planning",
    "Performance can improve"
)

engine.show_items()