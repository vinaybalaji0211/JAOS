from brain.strategic_planning_engine import StrategicPlanningEngine

engine = (
    StrategicPlanningEngine()
)

engine.create_plan(
    "Build JAOS",
    [
        "Complete Reasoning",
        "Build UI",
        "Deploy Platform",
        "Launch v1"
    ]
)

engine.show_plans()

engine.complete_plan(
    "Build JAOS"
)

engine.show_plans()