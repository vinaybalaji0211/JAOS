from brain.goal_conflict_resolver import GoalConflictResolver


goal_a = {
    "name": "Train model",
    "resource": "GPU",
    "focus_required": True,
    "interrupts_focus": False,
    "priority": 1
}

goal_b = {
    "name": "Run vision task",
    "resource": "GPU",
    "focus_required": False,
    "interrupts_focus": True,
    "priority": 3
}

GoalConflictResolver.show_conflicts(
    goal_a,
    goal_b
)