from jaos.executive.intent_registry import (
    ExecutiveIntentRegistry,
    IntentHandlerNotFoundError,
)
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutivePlan,
)


class ExecutivePlanner:
    """
    Converts executive intents into executable plans using registered handlers.
    """

    def __init__(self, registry: ExecutiveIntentRegistry) -> None:
        self.registry = registry

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        try:
            return self.registry.create_plan(intent)
        except IntentHandlerNotFoundError:
            return ExecutivePlan(
                intent=intent,
                steps=(),
            )