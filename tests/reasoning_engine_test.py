from brain.intent_classifier import IntentClassifier
from brain.planner_engine import PlannerEngine
from brain.reasoning_engine import ReasoningEngine

goal = (

    "Build an independent AI operating system"

)

intent = (

    IntentClassifier.classify(

        goal

    )

)

plan_data = (

    PlannerEngine.create_plan(

        intent,

        goal

    )

)

ReasoningEngine.show_reasoning(

    plan_data

)