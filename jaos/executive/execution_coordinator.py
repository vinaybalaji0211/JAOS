from jaos.executive.models import ExecutivePlan, ExecutiveResponse
from jaos.executive.telemetry.metrics import ExecutiveMetrics
from jaos.tools.tool_manager import ToolManager
from jaos.tools.tool_models import ToolRequest


class ExecutionCoordinator:
    """
    Executes executive plans through the Tool Platform.
    """

    def __init__(
        self,
        tool_manager: ToolManager,
        metrics: ExecutiveMetrics | None = None,
    ) -> None:
        self.tool_manager = tool_manager
        self.metrics = metrics or ExecutiveMetrics()

    def execute(self, plan: ExecutivePlan) -> ExecutiveResponse:
        step_count = len(plan.steps)

        if not plan.steps:
            self.metrics.record_failure(step_count)
            return ExecutiveResponse(
                success=False,
                message="I don't know how to handle that request yet.",
            )

        last_output = None

        for step in plan.steps:
            if step.requires_approval and not step.approved:
                self.metrics.record_failure(step_count)
                return ExecutiveResponse(
                    success=False,
                    message="Approval required. Add --confirm to approve this action.",
                )

            result = self.tool_manager.execute(
                ToolRequest(
                    tool_name=step.tool_name,
                    payload=step.payload,
                    approved=step.approved,
                )
            )

            if not result.success:
                self.metrics.record_failure(step_count)
                return ExecutiveResponse(
                    success=False,
                    message=result.error or "Tool execution failed.",
                )

            last_output = result.output

        self.metrics.record_success(step_count)

        return ExecutiveResponse(
            success=True,
            message="Task completed successfully.",
            output=last_output,
        )