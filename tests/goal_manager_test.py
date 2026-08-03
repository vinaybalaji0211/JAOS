from brain.goal_manager import GoalManager

manager = GoalManager()

manager.add_goal(
    "Build Iron-Man-level JARVIS",
    priority=1
)

manager.add_goal(
    "Improve security layer",
    priority=2
)

manager.update_progress(
    "Build Iron-Man-level JARVIS",
    40
)

manager.update_status(
    "Improve security layer",
    "PAUSED"
)

manager.show_goals()