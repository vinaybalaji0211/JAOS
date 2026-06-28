from executive_brain.common.enums import Priority, LifecycleStatus
from executive_brain.models.goal_model import GoalModel
from executive_brain.registries.goal_registry import GoalRegistry


registry = GoalRegistry()

goal = GoalModel(
    goal_name="VS Code Running",
    priority=Priority.HIGH,
    status=LifecycleStatus.ACTIVE,
    related_decision_id="DEC-001",
    success_criteria="VS Code process is active."
)

goal.add_metadata(
    "application",
    "VS Code"
)

registry.add_goal(
    goal
)

print("Count:", registry.count())
print("Exists:", registry.exists(goal.goal_id))

stored = registry.get_goal(goal.goal_id)
print("Retrieved:", stored.to_dict())

print("By Status:", len(registry.get_by_status(LifecycleStatus.ACTIVE)))
print("By Priority:", len(registry.get_by_priority(Priority.HIGH)))
print("By Decision:", len(registry.get_by_decision("DEC-001")))
print("Active:", len(registry.get_active_goals()))

registry.remove_goal(goal.goal_id)

print("Final Count:", registry.count())