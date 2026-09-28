from executive_brain.common.enums import LifecycleStatus
from executive_brain.registries.base_registry import BaseRegistry


class IntentRegistry(BaseRegistry):
    """
    Registry responsible for storing IntentModel objects.
    """

    def __init__(self):
        super().__init__()

    def get_by_type(self, intent_type):
        return [
            intent
            for intent in self.list_all()
            if getattr(intent, "intent_type", None) == intent_type
        ]

    def get_active_intents(self):
        return [
            intent
            for intent in self.list_all()
            if getattr(intent, "status", None) == LifecycleStatus.ACTIVE
        ]