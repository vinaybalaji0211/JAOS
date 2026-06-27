from logs.logger import logger


class ExecutionStrategySelector:

    @staticmethod
    def select_strategy(
            task_count,
            risk_level,
            requires_agents):

        if risk_level == "HIGH":

            strategy = "SAFE_MODE"

        elif requires_agents:

            strategy = "MULTI_AGENT"

        elif task_count > 3:

            strategy = "PARALLEL"

        else:

            strategy = "SEQUENTIAL"

        logger.info(
            f"Execution strategy selected: {strategy}"
        )

        return strategy

    @staticmethod
    def show_strategy(
            task_count,
            risk_level,
            requires_agents):

        strategy = (
            ExecutionStrategySelector
            .select_strategy(
                task_count,
                risk_level,
                requires_agents
            )
        )

        print("\nExecution Strategy:")

        print(strategy)