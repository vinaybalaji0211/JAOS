from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class AIProviderManager(BasePlatformService):
    """Runtime-managed AI provider manager."""

    SERVICE_NAME = "ai_provider_manager"

    def __init__(self, runtime=None):
        self.providers = {}

        super().__init__(runtime)

    def register_provider(self, name, status):
        self.providers[name] = status

        logger.info(f"AI Provider Registered: {name}")

        if self.runtime is not None:
            self.runtime.events.publish(
                "ai_provider_registered",
                {
                    "name": name,
                    "status": status,
                },
            )

    def provider_status(self, name):
        return self.providers.get(name, "UNKNOWN")

    def show_providers(self):
        print("\nAI Providers\n")

        if not self.providers:
            print("No providers registered.")
            return

        for provider, status in self.providers.items():
            print(f"{provider}: {status}")