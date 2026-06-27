import json
import os

from logs.logger import logger


class ProviderRouter:

    PROVIDER_FILE = "config/providers.json"

    def __init__(self):

        self.providers = self.load_providers()

    def load_providers(self):

        if not os.path.exists(
                self.PROVIDER_FILE):

            logger.warning(
                "Provider config not found."
            )

            return {}

        with open(
                self.PROVIDER_FILE,
                "r",
                encoding="utf-8") as file:

            providers = json.load(file)

        logger.info(
            "Providers loaded from config."
        )

        return providers

    def register_provider(
            self,
            name,
            provider_type,
            capabilities,
            priority=5):

        self.providers[name.lower()] = {
            "type": provider_type,
            "status": "AVAILABLE",
            "priority": priority,
            "capabilities": capabilities
        }

        self.save_providers()

        logger.info(
            f"Provider registered: {name}"
        )

    def save_providers(self):

        os.makedirs(
            "config",
            exist_ok=True
        )

        with open(
                self.PROVIDER_FILE,
                "w",
                encoding="utf-8") as file:

            json.dump(
                self.providers,
                file,
                indent=4
            )

        logger.info(
            "Providers saved to config."
        )

    def recommend_provider(self, task_type):

        task_type = task_type.lower()

        matches = []

        for name, details in self.providers.items():

            if details["status"] != "AVAILABLE":

                continue

            capabilities = details.get(
                "capabilities",
                []
            )

            if task_type in capabilities:

                matches.append(
                    (
                        name,
                        details["priority"]
                    )
                )

        if not matches:

            logger.warning(
                f"No provider found for task: {task_type}"
            )

            return None

        matches.sort(
            key=lambda item: item[1]
        )

        best_provider = matches[0][0]

        logger.info(
            f"Best provider for {task_type}: {best_provider}"
        )

        return best_provider

    def select_provider(self, mode="default"):

        if mode == "offline":

            return self.recommend_provider(
                "offline"
            )

        if mode == "coding":

            return self.recommend_provider(
                "coding"
            )

        if mode == "vision":

            return self.recommend_provider(
                "vision"
            )

        if mode == "writing":

            return self.recommend_provider(
                "writing"
            )

        return self.recommend_provider(
            "general"
        )

    def show_providers(self):

        print("\nAI Providers:")

        if not self.providers:

            print("No providers found.")

            return

        for name, details in self.providers.items():

            print(
                f"{name}: "
                f"{details['status']} | "
                f"{details['type']} | "
                f"priority={details['priority']} | "
                f"capabilities={details['capabilities']}"
            )