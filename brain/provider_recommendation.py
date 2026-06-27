from brain.provider_router import ProviderRouter
from logs.logger import logger


class ProviderRecommendation:

    @staticmethod
    def recommend(task_type):

        router = ProviderRouter()

        provider = router.select_provider(
            task_type
        )

        if provider is None:

            logger.warning(
                f"No provider recommendation found for {task_type}"
            )

            return {
                "task_type": task_type,
                "provider": None,
                "reason": "No matching provider found"
            }

        reason = (
            f"{provider} supports {task_type} tasks "
            "based on provider capabilities"
        )

        logger.info(
            f"Provider recommended: {provider}"
        )

        return {
            "task_type": task_type,
            "provider": provider,
            "reason": reason
        }

    @staticmethod
    def show_recommendation(task_type):

        result = ProviderRecommendation.recommend(
            task_type
        )

        print("\nProvider Recommendation:")

        print(
            f"Task Type: {result['task_type']}"
        )

        print(
            f"Provider: {result['provider']}"
        )

        print(
            f"Reason: {result['reason']}"
        )