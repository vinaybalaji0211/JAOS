from brain.task_delegation_engine import (
    TaskDelegationEngine
)

engine = (
    TaskDelegationEngine()
)

engine.delegate_task(
    "Extract PDF Content",
    "ResearchAgent",
    "DocumentAgent"
)

engine.delegate_task(
    "Security Review",
    "ExecutiveBrain",
    "SecurityAgent"
)

engine.complete_task(
    "Extract PDF Content"
)

engine.show_delegations()