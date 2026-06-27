from brain.learning_manager import LearningManager
from brain.experience_replay_engine import ExperienceReplayEngine
from brain.pattern_discovery_engine import PatternDiscoveryEngine
from brain.provider_performance_learning import (
    ProviderPerformanceLearning
)
from brain.strategy_optimizer import StrategyOptimizer
from brain.curiosity_engine import CuriosityEngine
from brain.autonomous_improvement_planner import (
    AutonomousImprovementPlanner
)


print("\n=== PHASE 6 INTEGRATION TEST ===\n")

# Learning
learning = LearningManager()

learning.learn(
    "failures",
    "GPU memory overflow"
)

learning.learn(
    "failures",
    "GPU memory overflow"
)

learning.learn(
    "successes",
    "Gemini reasoning success"
)

learning.show_learning()

# Experience Replay
experiences = [

    {
        "task": "YOLO Training",
        "result": "FAILED",
        "lesson": "Use batch size 4"
    },

    {
        "task": "Reasoning",
        "result": "SUCCESS",
        "lesson": "Use Gemini"
    }

]

ExperienceReplayEngine.show_replay(
    experiences
)

# Pattern Discovery

events = [

    "GPU memory overflow",

    "GPU memory overflow",

    "Gemini reasoning success",

    "GPU memory overflow"

]

PatternDiscoveryEngine.show_patterns(
    events
)

# Provider Learning

providers = (
    ProviderPerformanceLearning()
)

providers.record(
    "OpenAI",
    "coding",
    True
)

providers.record(
    "Gemini",
    "reasoning",
    True
)

providers.record(
    "Gemini",
    "reasoning",
    True
)

providers.show_stats()

# Strategy Optimizer

StrategyOptimizer.show_decision(
    success_count=3,
    failure_count=1,
    confidence=90
)

# Curiosity

questions = (
    CuriosityEngine.generate_questions(

        failures=[
            "GPU memory overflow"
        ],

        missing_capabilities=[
            "vision"
        ],

        unknown_topics=[
            "computer vision"
        ]

    )
)

CuriosityEngine.show_questions(

    failures=[
        "GPU memory overflow"
    ],

    missing_capabilities=[
        "vision"
    ],

    unknown_topics=[
        "computer vision"
    ]

)

# Autonomous Improvement

AutonomousImprovementPlanner.show_plan(

    repeated_failures=[
        "GPU memory overflow"
    ],

    missing_capabilities=[
        "vision"
    ],

    curiosity_questions=questions

)

print("\n=== PHASE 6 COMPLETE ===")