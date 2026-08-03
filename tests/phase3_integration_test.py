from brain.brain_state_manager import BrainStateManager
from brain.goal_tracker import GoalTracker
from brain.hidden_requirement_detector import HiddenRequirementDetector
from brain.proactive_suggestions import ProactiveSuggestions
from brain.reasoning_trace_logger import ReasoningTraceLogger
from brain.task_decomposer import TaskDecomposer
from memory.memory_categories import MemoryCategories
from memory.memory_manager import MemoryManager
from memory.memory_search import MemorySearch

print("\n========== PHASE 3 INTEGRATION TEST ==========")

# Brain state
brain = BrainStateManager()

brain.set_state("PLANNING")

brain.show_state()

# Memory
manager = MemoryManager()

manager.remember_short_term(
    "Phase 3 integration test running"
)

manager.remember_long_term(
    "Phase 3 integration completed"
)

manager.show_short_term()

# Goal
GoalTracker.add_goal(
    "Release JARVIS OS v0.3"
)

GoalTracker.show_goals()

# Task decomposition
TaskDecomposer.show_tasks(
    "Build JARVIS OS"
)

# Hidden requirements
HiddenRequirementDetector.show_missing(
    "Build AI app"
)

# Proactive suggestions
ProactiveSuggestions.show_suggestions(
    "phase memory goal"
)

# Category
MemoryCategories.show_category(
    "Phase 3 architecture completed"
)

# Search
MemorySearch.show_results(
    "Phase 3"
)

# Reasoning
ReasoningTraceLogger.record(
    "Release JARVIS OS v0.3",
    "All brain and memory modules are operational"
)

ReasoningTraceLogger.show()

print("\n========== TEST COMPLETE ==========")