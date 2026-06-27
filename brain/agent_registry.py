from logs.logger import logger


class AgentRegistry:

    def __init__(self):
        self.agents = {}

    def register_agent(
            self,
            name,
            role,
            capabilities=None,
            status="AVAILABLE"):

        if capabilities is None:
            capabilities = []

        self.agents[name] = {
            "role": role,
            "capabilities": capabilities,
            "status": status
        }

        logger.info(f"Agent registered: {name}")

    def update_status(
            self,
            name,
            status):

        if name in self.agents:
            self.agents[name]["status"] = status
            logger.info(f"Agent status updated: {name}")

    def get_agent(self, name):
        return self.agents.get(name)

    def show_agents(self):
        print("\nAgent Registry:\n")

        if not self.agents:
            print("No agents registered.")
            return

        for name, details in self.agents.items():
            print(f"Agent: {name}")
            print(f"Role: {details['role']}")
            print(f"Capabilities: {details['capabilities']}")
            print(f"Status: {details['status']}")
            print()