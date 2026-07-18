from abc import ABC, abstractmethod

from jaos.executive.models import ExecutiveIntent, ExecutivePlan


class ExecutiveIntentHandler(ABC):
    """
    Base contract for executive intent handlers.

    Each handler knows how to convert one intent type into an executable plan.
    """

    @abstractmethod
    def can_handle(self, intent: ExecutiveIntent) -> bool:
        """Return True if this handler supports the intent."""

    @abstractmethod
    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        """Create an executable plan for the intent."""