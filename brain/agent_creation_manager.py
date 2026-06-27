from logs.logger import logger


class AgentCreationManager:

    def __init__(self):

        self.created_agents = {}

    def create_agent(
            self,
            agent_name,
            purpose,
            capabilities=None):

        if capabilities is None:
            capabilities = []

        self.created_agents[agent_name] = {
            "purpose": purpose,
            "capabilities": capabilities,
            "status": "CREATED"
        }

        logger.info(
            f"Agent created: {agent_name}"
        )

    def show_created_agents(self):

        print("\nAgent Creation Manager:\n")

        if not self.created_agents:
            print("No agents created.")
            return

        for name, details in self.created_agents.items():
            print(f"Agent: {name}")
            print(f"Purpose: {details['purpose']}")
            print(f"Capabilities: {details['capabilities']}")
            print(f"Status: {details['status']}")
            print()