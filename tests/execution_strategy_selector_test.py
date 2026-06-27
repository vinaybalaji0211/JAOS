from brain.execution_strategy_selector import (
    ExecutionStrategySelector
)


ExecutionStrategySelector.show_strategy(
    task_count=2,
    risk_level="LOW",
    requires_agents=False
)

ExecutionStrategySelector.show_strategy(
    task_count=5,
    risk_level="LOW",
    requires_agents=False
)

ExecutionStrategySelector.show_strategy(
    task_count=3,
    risk_level="LOW",
    requires_agents=True
)

ExecutionStrategySelector.show_strategy(
    task_count=3,
    risk_level="HIGH",
    requires_agents=True
)