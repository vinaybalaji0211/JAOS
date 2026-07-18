from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class RenameFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for renaming files.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.RENAME_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="rename_file",
                    payload={
                        "source": intent.arguments["source"],
                        "new_name": intent.arguments["new_name"],
                    },
                    requires_approval=False,
                ),
            ),
        )