from logs.logger import logger


class AgentDeploymentManager:

    def __init__(self):

        self.deployed_agents = {}

    def deploy_agent(
            self,
            agent_name):

        self.deployed_agents[
            agent_name
        ] = "DEPLOYED"

        logger.info(
            f"Agent deployed: "
            f"{agent_name}"
        )

    def activate_agent(
            self,
            agent_name):

        if agent_name in (
                self.deployed_agents):

            self.deployed_agents[
                agent_name
            ] = "ACTIVE"

    def deactivate_agent(
            self,
            agent_name):

        if agent_name in (
                self.deployed_agents):

            self.deployed_agents[
                agent_name
            ] = "INACTIVE"

    def show_agents(self):

        print(
            "\nAgent Deployment Manager:\n"
        )

        if not self.deployed_agents:

            print(
                "No deployed agents."
            )

            return

        for agent, status in (
                self.deployed_agents.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                f"Status: {status}"
            )

            print()