from jaos.executive.diagnostics.models import DiagnosticStatus
from jaos.executive.intent_registry import ExecutiveIntentRegistry


class PlannerStatusProvider:
    """
    Reports diagnostics for the Executive Planner.
    """

    def __init__(self, registry: ExecutiveIntentRegistry) -> None:
        self.registry = registry

    def get_status(self) -> DiagnosticStatus:
        handlers = self.registry.list_handlers()

        return DiagnosticStatus(
            component="Executive Planner",
            healthy=bool(handlers),
            message="Planner is ready."
            if handlers
            else "Planner has no registered intent handlers.",
            details={
                "planning_mode": "registry-driven",
                "registered_handler_count": len(handlers),
            },
        )