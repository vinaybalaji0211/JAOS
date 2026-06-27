from brain.response_strategy_manager import (
    ResponseStrategyManager
)

manager = ResponseStrategyManager()

manager.show_strategy()

manager.set_strategy(
    "TECHNICAL"
)

manager.show_strategy()

manager.set_strategy(
    "EXECUTIVE"
)

manager.show_strategy()