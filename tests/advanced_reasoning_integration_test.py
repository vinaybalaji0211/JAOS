from brain.advanced_reasoning_core import (
    AdvancedReasoningCore
)

from brain.multi_step_reasoning_engine import (
    MultiStepReasoningEngine
)

from brain.decision_analysis_engine import (
    DecisionAnalysisEngine
)

from brain.strategic_planning_engine import (
    StrategicPlanningEngine
)

from brain.hypothesis_generation_engine import (
    HypothesisGenerationEngine
)

from brain.reflective_reasoning_engine import (
    ReflectiveReasoningEngine
)

print("\n=== ADVANCED REASONING TEST ===\n")

# Core
core = AdvancedReasoningCore()

core.start_reasoning(
    "Optimize JAOS",
    "Strategic Reasoning"
)

# Multi-step
reason = MultiStepReasoningEngine()

reason.create_chain(
    "Optimize JAOS",
    [
        "Analyze",
        "Generate Ideas",
        "Evaluate",
        "Recommend"
    ]
)

# Decision
decision = DecisionAnalysisEngine()

decision.analyze(
    "Choose AI Provider",
    [
        "OpenAI",
        "Gemini",
        "Local"
    ],
    "OpenAI"
)

# Planning
planner = StrategicPlanningEngine()

planner.create_plan(
    "JAOS v1 Alpha",
    [
        "Complete Reasoning",
        "Infrastructure",
        "Workflow",
        "Dashboard"
    ]
)

# Hypothesis
hypothesis = HypothesisGenerationEngine()

hypothesis.generate(
    "Slow Performance",
    [
        "GPU",
        "RAM",
        "Storage",
        "Background Apps"
    ]
)

# Reflection
reflection = ReflectiveReasoningEngine()

reflection.reflect(
    "Optimize JAOS",
    ["Architecture is modular"],
    ["Need performance data"],
    "Benchmark before optimization"
)

print("\n=== REASONING PIPELINE COMPLETE ===")