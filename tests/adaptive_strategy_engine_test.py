from brain.adaptive_strategy_engine import (
    AdaptiveStrategyEngine
)

engine = AdaptiveStrategyEngine()

engine.show_strategy()

engine.adapt(
    "AVERAGE"
)

engine.show_strategy()

engine.adapt(
    "EXCELLENT"
)

engine.show_strategy()