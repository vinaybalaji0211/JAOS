from brain.goal_hierarchy_engine import (
    GoalHierarchyEngine
)


engine = GoalHierarchyEngine()

engine.add_goal(

    "Build Independent 24/7 AI OS",

    priority=1

)

engine.add_goal(

    "Meta-Cognition",

    priority=2,

    parent="Build Independent 24/7 AI OS"

)

engine.add_goal(

    "World Model",

    priority=3,

    parent="Build Independent 24/7 AI OS"

)

engine.add_goal(

    "Continuous Learning",

    priority=4,

    parent="Build Independent 24/7 AI OS"

)

engine.show_goals()