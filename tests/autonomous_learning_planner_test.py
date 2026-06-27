from brain.autonomous_learning_planner import (
    AutonomousLearningPlanner
)

planner = (
    AutonomousLearningPlanner()
)

planner.create_plan(
    "Quantum Physics",
    [
        "Classical Physics",
        "Wave Mechanics",
        "Quantum States",
        "Schrodinger Equation",
        "Quantum Computing"
    ]
)

planner.show_plan(
    "Quantum Physics"
)