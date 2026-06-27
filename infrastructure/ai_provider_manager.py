from logs.logger import logger


class AIProviderManager:

    def __init__(self):

        self.providers = {}

    def register_provider(
            self,
            name,
            status):

        self.providers[
            name
        ] = status

        logger.info(
            f"AI Provider Registered: {name}"
        )

    def provider_status(
            self,
            name):

        return self.providers.get(
            name,
            "UNKNOWN"
        )

    def show_providers(self):

        print(
            "\nAI Providers\n"
        )

        if not self.providers:

            print(
                "No providers registered."
            )

            return

        for provider, status in (
                self.providers.items()):

            print(
                f"{provider}: {status}"
            )