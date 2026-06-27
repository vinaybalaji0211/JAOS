from brain.multi_step_reasoning_engine import (
    MultiStepReasoningEngine
)

engine = MultiStepReasoningEngine()

engine.create_chain(
    "Optimize YOLO Training",
    [
        "Check GPU usage",
        "Check dataset size",
        "Check batch size",
        "Check image size",
        "Recommend training settings"
    ]
)

engine.show_chain(
    "Optimize YOLO Training"
)