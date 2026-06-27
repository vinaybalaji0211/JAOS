from logs.logger import logger


class AgentCoordinator:

    def __init__(self):

        self.agent_tasks = {}

    def assign_task(
            self,
            agent_name,
            task):

        self.agent_tasks[agent_name] = {
            "task": task,
            "status": "ASSIGNED",
            "result": None
        }

        logger.info(
            f"Task assigned to {agent_name}"
        )

    def update_result(
            self,
            agent_name,
            result):

        if agent_name in self.agent_tasks:

            self.agent_tasks[agent_name]["result"] = result
            self.agent_tasks[agent_name]["status"] = "COMPLETED"

            logger.info(
                f"Result received from {agent_name}"
            )

    def show_tasks(self):

        print("\nAgent Coordinator:\n")

        if not self.agent_tasks:

            print("No agent tasks.")

            return

        for agent, details in self.agent_tasks.items():

            print(f"Agent: {agent}")
            print(f"Task: {details['task']}")
            print(f"Status: {details['status']}")
            print(f"Result: {details['result']}")
            print()