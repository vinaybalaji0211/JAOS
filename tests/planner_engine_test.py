from brain.intent_classifier import IntentClassifier
from brain.planner_engine import PlannerEngine


goal = "Build an independent AI operating system"

intent = IntentClassifier.classify(
    goal
)

PlannerEngine.show_plan(
    intent,
    goal
)