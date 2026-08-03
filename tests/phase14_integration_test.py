from brain.attention_manager import AttentionManager
from brain.context_manager import ContextManager
from brain.decision_engine import DecisionEngine
from brain.executive_controller import ExecutiveController
from brain.goal_manager import GoalManager
from brain.priority_engine import PriorityEngine

print("\n=== PHASE 14 INTEGRATION TEST ===\n")

controller = ExecutiveController()
controller.set_goal("Build Iron-Man-level JARVIS")
controller.set_state("EXECUTIVE")
controller.show_status()

attention = AttentionManager()
attention.focus_on("Executive Brain", "HIGH")
attention.show_focus()

priority = PriorityEngine()
priority.add_task("Security Review", "CRITICAL")
priority.add_task("Voice System", "HIGH")
priority.show_tasks()

goals = GoalManager()
goals.add_goal("Complete Phase 14", 1)
goals.update_progress("Complete Phase 14", 100)
goals.show_goals()

options = [
    {
        "name": "Safe Option",
        "priority": 20,
        "confidence": 90,
        "goal_alignment": 90,
        "resources_ok": True,
        "risk": "LOW"
    }
]

DecisionEngine.show_decision(options)

context = ContextManager()
context.update_context(
    "current_mode",
    "EXECUTIVE"
)
context.show_context()

print("\n=== PHASE 14 COMPLETE ===")