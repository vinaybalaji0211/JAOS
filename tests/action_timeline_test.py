from dashboard.action_timeline import (
    ActionTimeline
)

timeline = ActionTimeline()

timeline.add_action(
    "Development",
    "Git Manager",
    "Register Repository",
    "SUCCESS"
)

timeline.add_action(
    "Security",
    "Permission Manager",
    "Grant Permission",
    "SUCCESS"
)

timeline.show_timeline()