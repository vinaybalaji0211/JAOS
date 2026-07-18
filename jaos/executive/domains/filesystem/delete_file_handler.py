from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class DeleteFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for deleting files.

    Delete is dangerous and requires explicit approval.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.DELETE_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="delete_file",
                    payload={
                        "path": intent.arguments["path"],
                    },
                    requires_approval=True,
                    approved=bool(intent.arguments.get("approved", False)),
                ),
            ),
        )