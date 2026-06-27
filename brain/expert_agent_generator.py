from logs.logger import logger


class ExpertAgentGenerator:

    def __init__(self):

        self.agents = {}

    def create_agent(
            self,
            agent_name,
            capabilities):

        self.agents[
            agent_name
        ] = capabilities

        logger.info(
            f"Expert agent created: "
            f"{agent_name}"
        )

    def show_agents(self):

        print(
            "\nExpert Agent Generator:\n"
        )

        if not self.agents:

            print(
                "No expert agents."
            )

            return

        for agent, capabilities in (
                self.agents.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                "Capabilities:"
            )

            for capability in capabilities:

                print(
                    f" - {capability}"
                )

            print()