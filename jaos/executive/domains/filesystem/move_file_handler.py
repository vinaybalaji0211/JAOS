from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class MoveFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for moving files.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.MOVE_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="move_file",
                    payload={
                        "source": intent.arguments["source"],
                        "destination": intent.arguments["destination"],
                    },
                    requires_approval=False,
                ),
            ),
        )