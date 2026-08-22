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

        # parser_status and execution_status have no real failure condition
        # to check today (ParserStatusProvider/ExecutionStatusProvider report
        # a static, dependency-free capability, not a verified fact), so they
        # are surfaced in details but excluded from the aggregate: including
        # their unconditional healthy=True would let overall health be true
        # partly because a component merely exists.
        healthy = all(
            (
                handler_status.healthy,
                planner_status.healthy,
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