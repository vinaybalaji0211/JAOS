from brain.learning_priority_planner import (
    LearningPriorityPlanner
)

planner = (
    LearningPriorityPlanner()
)

planner.set_priority(
    "Cybersecurity",
    "HIGH"
)

planner.set_priority(
    "Quantum Physics",
    "MEDIUM"
)

planner.set_priority(
    "Machine Learning",
    "LOW"
)

planner.show_priorities()

print(
    planner.get_priority(
        "Cybersecurity"
    )
)