from brain.goal_progress_tracker import GoalProgressTracker

tracker = GoalProgressTracker()

tracker.add_goal(
    "Complete Executive Brain"
)

tracker.add_milestone(
    "Complete Executive Brain",
    "Finish Goal Layer"
)

tracker.add_milestone(
    "Complete Executive Brain",
    "Finish Decision Engine"
)

tracker.update_progress(
    "Complete Executive Brain",
    60
)

tracker.show_progress()