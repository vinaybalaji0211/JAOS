from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class BackupFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates a multi-step execution plan for backing up a file.

    Step 1: Copy source to destination.
    Step 2: Read destination to verify it exists and is readable.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.BACKUP_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        source = intent.arguments["source"]
        destination = intent.arguments["destination"]

        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="copy_file",
                    payload={
                        "source": source,
                        "destination": destination,
                    },
                    requires_approval=False,
                ),
                ExecutivePlanStep(
                    tool_name="read_file",
                    payload={
                        "path": destination,
                    },
                    requires_approval=False,
                ),
            ),
        )