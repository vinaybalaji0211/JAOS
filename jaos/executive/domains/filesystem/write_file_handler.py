from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class WriteFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for writing files.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.WRITE_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="write_file",
                    payload={
                        "path": intent.arguments["path"],
                        "content": intent.arguments["content"],
                    },
                    requires_approval=False,
                ),
            ),
        )