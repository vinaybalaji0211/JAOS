from brain.risk_evaluator import RiskEvaluator
from brain.reality_awareness_layer import RealityAwarenessLayer
from brain.resource_awareness_engine import ResourceAwarenessEngine
from brain.time_awareness_layer import TimeAwarenessLayer
from brain.supervisor_agent import SupervisorAgent
from brain.knowledge_conflict_detector import KnowledgeConflictDetector
from brain.confidence_estimator import ConfidenceEstimator
from brain.safety_decision_layer import SafetyDecisionLayer
from brain.reflection_engine import ReflectionEngine
from brain.feedback_collector import FeedbackCollector
from brain.meta_cognition import MetaCognition


print("\n=== PHASE 4 INTEGRATION TEST ===")

# Risk
risk = RiskEvaluator.evaluate(
    [
        "read_file"
    ]
)

# Reality
reality = RealityAwarenessLayer.assess(
    "Read project file",
    "HIGH",
    True,
    True
)

# Resources
resources = ResourceAwarenessEngine.assess_resources()

# Time
time_info = TimeAwarenessLayer.get_time_info()

# Supervisor
jarvis = SupervisorAgent()
jarvis.set_goal(
    "Build Independent 24/7 AI Operating System"
)
jarvis.set_task(
    "Phase 5 World Model"
)

# Conflict Detection
conflicts = KnowledgeConflictDetector.detect(
    []
)

# Confidence
confidence_report = (
    ConfidenceEstimator.estimate(
        95,
        95,
        95,
        95,
        100,
        len(conflicts)
    )
)

# Safety
decision = SafetyDecisionLayer.decide(
    risk,
    confidence_report["final_confidence"],
    len(conflicts),
    reality["feasible"],
    True
)

# Reflection
reflection = ReflectionEngine.reflect(
    "Phase 4 integration",
    "SUCCESS",
    [
        "All systems operational"
    ],
    "Continue roadmap",
    "Begin Phase 5"
)

# Feedback
collector = FeedbackCollector()

collector.add_experience(
    "Phase 4 Integration",
    "SUCCESS",
    "All modules working",
    "Proceed to Phase 5",
    "Begin World Model",
    confidence_report["final_confidence"],
    "Internal"
)

# Meta Cognition
meta = MetaCognition.analyze(
    strengths=[
        "Stable cognitive core"
    ],
    weaknesses=[
        "World model not implemented"
    ],
    strategy_change=
        "Proceed to Phase 5",
    provider_preference=
        "Dynamic",
    self_improvement_goal=
        "Build world understanding"
)

print("\n=== PHASE 4 COMPLETE ===")
print("Safety Decision:", decision)
print("Confidence:", confidence_report["final_confidence"])
print("Current Goal:", jarvis.current_goal)
print("Next:", reflection["next_action"])