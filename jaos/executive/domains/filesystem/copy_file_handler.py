from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class CopyFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for copying files.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.COPY_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="copy_file",
                    payload={
                        "source": intent.arguments["source"],
                        "destination": intent.arguments["destination"],
                    },
                    requires_approval=False,
                ),
            ),
        )