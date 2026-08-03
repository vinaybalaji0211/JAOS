from executive_brain.common.enums import Priority
from executive_brain.models.goal_model import GoalModel

goal = GoalModel(
    goal_name="VS Code Running",
    priority=Priority.HIGH,
    related_decision_id="DEC-001",
    success_criteria="VS Code process is active."
)

goal.add_metadata(
    "application",
    "VS Code"
)

print()
print(goal.to_dict())