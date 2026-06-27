from logs.logger import logger


class ProviderTransparency:

    def __init__(self):

        self.last_provider_info = None

    def record_provider(
            self,
            provider,
            model,
            reason,
            mode):

        self.last_provider_info = {

            "provider": provider,

            "model": model,

            "reason": reason,

            "mode": mode

        }

        logger.info(
            f"Provider transparency recorded: {provider}"
        )

    def show_last_provider(self):

        print("\nLast AI Provider Used:")

        if not self.last_provider_info:

            print("No provider information recorded.")

            return

        print(
            f"Provider: {self.last_provider_info['provider']}"
        )

        print(
            f"Model: {self.last_provider_info['model']}"
        )

        print(
            f"Reason: {self.last_provider_info['reason']}"
        )

        print(
            f"Mode: {self.last_provider_info['mode']}"
        )