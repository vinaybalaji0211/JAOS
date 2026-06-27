from executive_brain.common.enums import LifecycleStatus, Priority
from executive_brain.registries.base_registry import BaseRegistry


class GoalRegistry(BaseRegistry):
    """
    Registry responsible for storing GoalModel objects.
    """

    def __init__(self):
        super().__init__()

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