from brain.self_evaluation_engine import (
    SelfEvaluationEngine
)

engine = SelfEvaluationEngine()

engine.record_metric(
    "Security",
    95
)

engine.record_metric(
    "Memory",
    90
)

engine.record_metric(
    "Planning",
    88
)

engine.record_metric(
    "Recovery",
    92
)

engine.show_evaluation()