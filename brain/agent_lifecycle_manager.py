from logs.logger import logger


class AgentLifecycleManager:

    def __init__(self):

        self.agents = {}

    def create_agent(
            self,
            agent_name):

        self.agents[
            agent_name
        ] = "CREATED"

        logger.info(
            f"Agent created: {agent_name}"
        )

    def update_status(
            self,
            agent_name,
            status):

        if agent_name in self.agents:

            self.agents[
                agent_name
            ] = status

            logger.info(
                f"{agent_name} -> {status}"
            )

    def get_status(
            self,
            agent_name):

        return self.agents.get(
            agent_name
        )

    def show_agents(self):

        print(
            "\nAgent Lifecycle Manager:\n"
        )

        if not self.agents:

            print(
                "No agents."
            )

            return

        for agent, status in (
                self.agents.items()):

            print(
                f"{agent}: {status}"
            )