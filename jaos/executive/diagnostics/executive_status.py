from jaos.executive.diagnostics.execution_status import ExecutionStatusProvider
from jaos.executive.diagnostics.handler_status import HandlerStatusProvider
from jaos.executive.diagnostics.models import DiagnosticStatus
from jaos.executive.diagnostics.parser_status import ParserStatusProvider
from jaos.executive.diagnostics.planner_status import PlannerStatusProvider
from jaos.executive.intent_registry import ExecutiveIntentRegistry


class ExecutiveStatusProvider:
    """
    Reports overall Executive Platform health.
    """

    def __init__(self, registry: ExecutiveIntentRegistry) -> None:
        self.registry = registry

    def get_status(self) -> DiagnosticStatus:
        handler_status = HandlerStatusProvider(self.registry).get_status()
        parser_status = ParserStatusProvider().get_status()
        planner_status = PlannerStatusProvider(self.registry).get_status()
        execution_status = ExecutionStatusProvider().get_status()

        healthy = all(
            (
                handler_status.healthy,
                parser_status.healthy,
                planner_status.healthy,
                execution_status.healthy,
            )
        )

        return DiagnosticStatus(
            component="Executive Platform",
            healthy=healthy,
            message="Executive Platform is online."
            if healthy
            else "Executive Platform diagnostics reported issues.",
            details={
                "handlers": handler_status.details,
                "parser": parser_status.details,
                "planner": planner_status.details,
                "execution": execution_status.details,
            },
        )