from brain.autonomous_learning_planner import (
    AutonomousLearningPlanner
)

from brain.knowledge_curriculum_builder import (
    KnowledgeCurriculumBuilder
)

from brain.continuous_learning_engine import (
    ContinuousLearningEngine
)

from brain.domain_expertise_tracker import (
    DomainExpertiseTracker
)

from brain.learning_priority_planner import (
    LearningPriorityPlanner
)

from brain.capability_discovery_engine import (
    CapabilityDiscoveryEngine
)

print(
    "\n=== AUTONOMOUS LEARNING INTEGRATION TEST ===\n"
)

# Learning Planner

planner = AutonomousLearningPlanner()

planner.create_plan(
    "Quantum Physics",
    [
        "Classical Physics",
        "Wave Mechanics",
        "Quantum States"
    ]
)

planner.show_plan(
    "Quantum Physics"
)

# Curriculum

curriculum = (
    KnowledgeCurriculumBuilder()
)

curriculum.create_curriculum(
    "Quantum Physics",
    {
        "Level 1": [
            "Classical Physics"
        ],
        "Level 2": [
            "Wave Mechanics"
        ],
        "Level 3": [
            "Quantum States"
        ]
    }
)

curriculum.show_curriculum(
    "Quantum Physics"
)

# Continuous Learning

learning = (
    ContinuousLearningEngine()
)

learning.learn(
    "Classical Physics"
)

learning.learn(
    "Wave Mechanics"
)

learning.show_progress()

# Expertise

expertise = (
    DomainExpertiseTracker()
)

expertise.update_expertise(
    "Quantum Physics",
    40
)

expertise.show_expertise()

# Priorities

priority = (
    LearningPriorityPlanner()
)

priority.set_priority(
    "Quantum Physics",
    "HIGH"
)

priority.show_priorities()

# Capability Discovery

capability = (
    CapabilityDiscoveryEngine()
)

capability.register_capability(
    "Research Analysis"
)

capability.register_capability(
    "Quantum Expert",
    False
)

capability.show_capabilities()

print(
    capability.discover_gap(
        "Quantum Expert"
    )
)

print(
    "\n=== AUTONOMOUS LEARNING COMPLETE ==="
)