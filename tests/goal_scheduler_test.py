from brain.goal_scheduler import GoalScheduler

scheduler = GoalScheduler()

scheduler.schedule_goal(
    "Build Vision Layer",
    "weekly",
    priority=1
)

scheduler.schedule_goal(
    "Run health check",
    "daily",
    priority=2
)

scheduler.schedule_goal(
    "Memory consolidation",
    "nightly",
    priority=3
)

scheduler.show_goals()

scheduler.complete_goal(
    "Run health check"
)

scheduler.show_goals()