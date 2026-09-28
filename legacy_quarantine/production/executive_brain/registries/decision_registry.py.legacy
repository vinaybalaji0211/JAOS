from executive_brain.common.enums import LifecycleStatus
from executive_brain.registries.base_registry import BaseRegistry


class DecisionRegistry(BaseRegistry):
    """
    Registry responsible for storing DecisionModel objects.
    """

    def __init__(self):
        super().__init__()

    def get_by_type(self, decision_type):
        return [
            decision
            for decision in self.list_all()
            if getattr(decision, "decision_type", None) == decision_type
        ]

    def get_by_status(self, status: LifecycleStatus):
        return [
            decision
            for decision in self.list_all()
            if getattr(decision, "status", None) == status
        ]

    def get_active_decisions(self):
        return self.get_by_status(LifecycleStatus.ACTIVE)

    def get_by_intent(self, intent_id):
        return [
            decision
            for decision in self.list_all()
            if getattr(decision, "related_intent_id", None) == intent_id
        ]