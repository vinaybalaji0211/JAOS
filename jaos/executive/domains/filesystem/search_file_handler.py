from jaos.executive.intent_handler import ExecutiveIntentHandler
from jaos.executive.models import (
    ExecutiveIntent,
    ExecutiveIntentType,
    ExecutivePlan,
    ExecutivePlanStep,
)


class SearchFileIntentHandler(ExecutiveIntentHandler):
    """
    Creates execution plans for searching files.
    """

    def can_handle(self, intent: ExecutiveIntent) -> bool:
        return intent.intent_type == ExecutiveIntentType.SEARCH_FILE

    def create_plan(self, intent: ExecutiveIntent) -> ExecutivePlan:
        return ExecutivePlan(
            intent=intent,
            steps=(
                ExecutivePlanStep(
                    tool_name="search_file",
                    payload={
                        "root": intent.arguments["root"],
                        "pattern": intent.arguments["pattern"],
                        "max_results": 100,
                    },
                    requires_approval=False,
                ),
            ),
        )