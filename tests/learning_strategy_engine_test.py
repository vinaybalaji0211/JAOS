from brain.learning_strategy_engine import LearningStrategyEngine

recommendations = [
    "Improve weak area: Threat monitoring",
    "Fix repeated failure: Plugin timeout",
    "Improve Planning, current score is 65",
    "Improve Recovery, current score is 70"
]

LearningStrategyEngine.show_strategy(
    recommendations,
    priority_focus="executive_improvement"
)