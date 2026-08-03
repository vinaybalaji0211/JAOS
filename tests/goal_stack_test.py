from brain.goal_stack import GoalStack

stack = GoalStack()

stack.add_goal(
    "Provider optimization",
    4
)

stack.add_goal(
    "Memory consolidation",
    3
)

stack.add_goal(
    "Run health checks",
    2
)

stack.add_goal(
    "Build JARVIS OS",
    1
)

stack.show_goals()

print()

print(
    "Current Goal:",
    stack.get_current_goal()
)