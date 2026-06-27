from brain.provider_recommendation import ProviderRecommendation
from logs.logger import logger


class MultiProviderCollaboration:

    @staticmethod
    def collaborate(task_types):

        selected_providers = []

        for task_type in task_types:

            recommendation = ProviderRecommendation.recommend(
                task_type
            )

            provider = recommendation["provider"]

            if provider and provider not in selected_providers:

                selected_providers.append(
                    provider
                )

        logger.info(
            f"Multi-provider collaboration selected: {selected_providers}"
        )

        return selected_providers

    @staticmethod
    def show_collaboration(task_types):

        providers = MultiProviderCollaboration.collaborate(
            task_types
        )

        print("\nMulti-Provider Collaboration:")

        print(
            f"Task Types: {task_types}"
        )

        if not providers:

            print("No providers selected.")

        else:

            print("Selected Providers:")

            for index, provider in enumerate(
                    providers,
                    start=1):

                print(
                    f"{index}. {provider}"
                )