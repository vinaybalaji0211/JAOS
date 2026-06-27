from logs.logger import logger


class CognitiveLoadManager:

    @staticmethod
    def assess(
            active_tasks,
            active_agents,
            priority_pressure,
            system_load):

        load_score = (
            active_tasks * 10
            + active_agents * 15
            + priority_pressure
            + system_load
        )

        if load_score >= 100:
            state = "OVERLOADED"

        elif load_score >= 60:
            state = "BUSY"

        else:
            state = "NORMAL"

        logger.info(
            f"Cognitive load assessed: {state}"
        )

        return {
            "load_score": load_score,
            "state": state
        }

    @staticmethod
    def show_load(
            active_tasks,
            active_agents,
            priority_pressure,
            system_load):

        result = CognitiveLoadManager.assess(
            active_tasks,
            active_agents,
            priority_pressure,
            system_load
        )

        print("\nCognitive Load Manager:\n")
        print(f"Load Score: {result['load_score']}")
        print(f"State: {result['state']}")