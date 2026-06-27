from logs.logger import logger


class AgentManager:

    def __init__(self):

        self.agents = []

    def register_agent(self, agent_name):

        self.agents.append(
            agent_name
        )

        logger.info(
            f"Agent registered: {agent_name}"
        )

    def show_agents(self):

        print("\nRegistered Agents:")

        if not self.agents:

            print("No agents registered.")

        else:

            for index, agent in enumerate(
                    self.agents,
                    start=1):

                print(
                    f"{index}. {agent}"
                )

    def get_agents(self):

        return self.agents