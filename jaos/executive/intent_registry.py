from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import ExecutiveIntent, ExecutivePlan


class IntentHandlerNotFoundError(Exception):
    """Raised when no handler exists for an executive intent."""


class ExecutiveIntentRegistry:
    """
    Registry for executive intent handlers.
    """

    def __init__(self) -> None:
        self._handlers: list[ExecutiveIntentHandler] = []

    def register(self, handler: ExecutiveIntentHandler) -> None:
        self._handlers.append(handler)

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        for handler in self._handlers:
            if handler.can_handle(intent):
                return handler.create_plan(intent)

        raise IntentHandlerNotFoundError(
            f"No executive intent handler found for: {intent.intent_type}"
        )

    def list_handlers(self) -> tuple[str, ...]:
        return tuple(handler.__class__.__name__ for handler in self._handlers)