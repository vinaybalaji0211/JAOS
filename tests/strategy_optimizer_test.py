from brain.strategy_optimizer import StrategyOptimizer


StrategyOptimizer.show_decision(
    success_count=5,
    failure_count=1,
    confidence=90
)

StrategyOptimizer.show_decision(
    success_count=1,
    failure_count=4,
    confidence=40
)

StrategyOptimizer.show_decision(
    success_count=3,
    failure_count=2,
    confidence=75,
    resource_issue=True
)

StrategyOptimizer.show_decision(
    success_count=2,
    failure_count=2,
    confidence=60
)