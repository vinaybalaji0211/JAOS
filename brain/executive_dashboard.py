from logs.logger import logger


class ExecutiveDashboard:

    @staticmethod
    def show(
            goal,
            task,
            agent,
            priority,
            load,
            decision,
            system_mode):

        logger.info("Executive dashboard displayed.")

        print("\nExecutive Dashboard:\n")

        print(f"Goal: {goal}")
        print(f"Task: {task}")
        print(f"Agent: {agent}")
        print(f"Priority: {priority}")
        print(f"Cognitive Load: {load}")
        print(f"Decision: {decision}")
        print(f"System Mode: {system_mode}")