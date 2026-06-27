from logs.logger import logger


class AIProviderManager:

    def __init__(self):
        self.providers = {}

    def register_provider(
            self,
            name,
            capabilities=None,
            cost_level="UNKNOWN",
            speed="UNKNOWN",
            reliability="UNKNOWN",
            status="AVAILABLE"):

        if capabilities is None:
            capabilities = []

        self.providers[name] = {
            "capabilities": capabilities,
            "cost_level": cost_level,
            "speed": speed,
            "reliability": reliability,
            "status": status
        }

        logger.info(f"AI provider registered: {name}")

    def update_status(
            self,
            name,
            status):

        if name in self.providers:
            self.providers[name]["status"] = status
            logger.info(f"Provider status updated: {name}")

    def get_provider(self, name):
        return self.providers.get(name)

    def show_providers(self):

        print("\nAI Provider Manager:\n")

        if not self.providers:
            print("No AI providers registered.")
            return

        for name, details in self.providers.items():
            print(f"Provider: {name}")
            print(f"Capabilities: {details['capabilities']}")
            print(f"Cost Level: {details['cost_level']}")
            print(f"Speed: {details['speed']}")
            print(f"Reliability: {details['reliability']}")
            print(f"Status: {details['status']}")
            print()