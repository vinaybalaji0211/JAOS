from logs.logger import logger


class AIResearchAgent:

    KNOWN_MODELS = {
        "openai": {
            "strength": "reasoning and coding",
            "type": "cloud"
        },
        "gemini": {
            "strength": "vision and multimodal",
            "type": "cloud"
        },
        "deepseek": {
            "strength": "coding and low cost",
            "type": "cloud"
        },
        "ollama": {
            "strength": "offline and local models",
            "type": "local"
        },
        "claude": {
            "strength": "writing and analysis",
            "type": "cloud"
        },
        "qwen": {
            "strength": "coding and local reasoning",
            "type": "local"
        },
        "mistral": {
            "strength": "fast lightweight reasoning",
            "type": "cloud"
        }
    }

    @staticmethod
    def show_models():

        print("\nKnown AI Models:\n")

        for name, details in AIResearchAgent.KNOWN_MODELS.items():

            print(
                f"{name} | "
                f"Strength={details['strength']} | "
                f"Type={details['type']}"
            )

    @staticmethod
    def recommend_model(task):

        task = task.lower()

        for name, details in AIResearchAgent.KNOWN_MODELS.items():

            if task in details["strength"]:

                logger.info(
                    f"Recommended AI model: {name}"
                )

                return name

        logger.info(
            "No AI model recommendation found."
        )

        return "No recommendation found"