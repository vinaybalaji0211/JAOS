from executive_brain.common.enums import LifecycleStatus, Priority
from executive_brain.models.goal_model import GoalModel
from executive_brain.registries.base_registry import BaseRegistry


class GoalRegistry(BaseRegistry):
    """
    Registry responsible for storing GoalModel objects.
    """

    def __init__(self):
        super().__init__()

    def add_goal(self, goal: GoalModel):
        if not isinstance(goal, GoalModel):
            raise TypeError("goal must be an instance of GoalModel.")

        self.add(goal.goal_id, goal)

    def get_goal(self, goal_id: str):
        return self.get(goal_id)

    def update_goal(self, goal: GoalModel):
        if not isinstance(goal, GoalModel):
            raise TypeError("goal must be an instance of GoalModel.")

        self.update(goal.goal_id, goal)

    def remove_goal(self, goal_id: str):
        return self.remove(goal_id)

    def list_goals(self):
        return self.list_all()

    def get_by_status(self, status: LifecycleStatus):
        return [
            goal
            for goal in self.list_all()
            if getattr(goal, "status", None) == status
        ]

    def get_by_priority(self, priority: Priority):
        return [
            goal
            for goal in self.list_all()
            if getattr(goal, "priority", None) == priority
        ]

    def get_by_decision(self, decision_id):
        return [
            goal
            for goal in self.list_all()
            if getattr(goal, "related_decision_id", None) == decision_id
        ]

    def get_active_goals(self):
        return self.get_by_status(LifecycleStatus.ACTIVE)