from jaos.ai import AIManager
from jaos.executive.ai import ExecutiveAIGateway
from jaos.executive.bootstrap.handler_loader import build_intent_registry
from jaos.executive.diagnostics.executive_status import ExecutiveStatusProvider
from jaos.executive.diagnostics.models import DiagnosticStatus
from jaos.executive.execution_coordinator import ExecutionCoordinator
from jaos.executive.intent_parser import ExecutiveIntentParser
from jaos.executive.models import ExecutiveIntentType, ExecutiveResponse
from jaos.executive.planner import ExecutivePlanner
from jaos.executive.reasoning import AIReasoningService
from jaos.executive.telemetry.metrics import ExecutiveMetrics
from jaos.tools.tool_manager import ToolManager


class ExecutiveController:
    """
    Front door for JAOS executive orchestration.

    Deterministic requests are handled by the Executive pipeline.
    Unknown requests can be routed to AI reasoning through ExecutiveAIGateway
    if AI is available.
    """

    def __init__(
        self,
        tool_manager: ToolManager,
        ai_manager: AIManager | None = None,
        ai_gateway: ExecutiveAIGateway | None = None,
    ) -> None:
        self.intent_registry = build_intent_registry()
        self.intent_parser = ExecutiveIntentParser()
        self.planner = ExecutivePlanner(self.intent_registry)
        self.metrics = ExecutiveMetrics()
        self.execution_coordinator = ExecutionCoordinator(
            tool_manager,
            metrics=self.metrics,
        )
        self.status_provider = ExecutiveStatusProvider(self.intent_registry)

        gateway = ai_gateway
        if gateway is None and ai_manager is not None:
            gateway = ExecutiveAIGateway(ai_manager)

        self.ai_reasoning_service = (
            AIReasoningService(gateway) if gateway is not None else None
        )

    def process(self, user_input: str) -> ExecutiveResponse:
        intent = self.intent_parser.parse(user_input)

        if intent.intent_type == ExecutiveIntentType.UNKNOWN:
            if self.ai_reasoning_service is not None:
                return self.ai_reasoning_service.reason(user_input)

            return ExecutiveResponse(
                success=False,
                message="I don't know how to handle that request yet.",
            )

        plan = self.planner.create_plan(intent)
        return self.execution_coordinator.execute(plan)

    def get_status(self) -> DiagnosticStatus:
        return self.status_provider.get_status()

    def get_metrics(self) -> ExecutiveMetrics:
        return self.metrics