from brain.long_term_planner import LongTermPlanner


planner = LongTermPlanner()

planner.add_plan(
    "Complete Executive Brain",
    "weekly",
    "Finish Phase 14"
)

planner.add_plan(
    "Build Iron-Man-level JARVIS",
    "long-term",
    "Create strong, secure, advanced AI OS"
)

planner.update_status(
    "Complete Executive Brain",
    "IN_PROGRESS"
)

planner.show_plans()