from brain.goal_hierarchy_manager import GoalHierarchyManager


manager = GoalHierarchyManager()

manager.add_goal("Build Iron-Man-level JARVIS")

manager.add_subgoal(
    "Build Iron-Man-level JARVIS",
    "Executive Brain"
)

manager.add_task(
    "Build Iron-Man-level JARVIS",
    "Executive Brain",
    "Implement Decision Engine"
)

manager.add_task(
    "Build Iron-Man-level JARVIS",
    "Executive Brain",
    "Implement Context Manager"
)

manager.show_hierarchy()