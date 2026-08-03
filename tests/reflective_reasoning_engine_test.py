from brain.reflective_reasoning_engine import ReflectiveReasoningEngine

engine = (
    ReflectiveReasoningEngine()
)

engine.reflect(
    "Optimize YOLO Training",
    [
        "Identified possible bottlenecks",
        "Generated multiple hypotheses"
    ],
    [
        "No real GPU data checked yet",
        "No benchmark results used"
    ],
    "Collect system metrics before final recommendation"
)

engine.show_reflections()