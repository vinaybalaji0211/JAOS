from logs.logger import logger


class AgentMarketplace:

    def __init__(self):
        self.agents = {}

    def add_agent(self, agent_name, version, role):
        self.agents[agent_name] = {
            "version": version,
            "role": role,
            "status": "INSTALLED"
        }

        logger.info(f"Agent installed: {agent_name}")

    def remove_agent(self, agent_name):
        if agent_name in self.agents:
            self.agents[agent_name]["status"] = "REMOVED"
            logger.info(f"Agent removed: {agent_name}")

    def show_agents(self):
        print("\nAgent Marketplace:\n")

        if not self.agents:
            print("No agents installed.")
            return

        for agent, details in self.agents.items():
            print(
                f"{agent} | "
                f"Version {details['version']} | "
                f"Role: {details['role']} | "
                f"{details['status']}"
            )