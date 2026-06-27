from logs.logger import logger


class IntentClassifier:

    INTENTS = {

        "QUESTION": [
            "what",
            "why",
            "how",
            "when"
        ],

        "TASK": [
            "build",
            "create",
            "make",
            "implement"
        ],

        "AUTOMATION": [
            "automate",
            "schedule",
            "monitor"
        ],

        "MEMORY": [
            "remember",
            "recall",
            "history"
        ],

        "SYSTEM": [
            "status",
            "health",
            "diagnostics"
        ],

        "RESEARCH": [
            "research",
            "study",
            "analyze"
        ],

        "FILE": [
            "file",
            "folder",
            "directory"
        ]
    }

    @staticmethod
    def classify(text):

        text = text.lower()

        for intent, keywords in (
                IntentClassifier
                .INTENTS.items()):

            for keyword in keywords:

                if keyword in text:

                    logger.info(
                        f"Intent detected: {intent}"
                    )

                    return intent

        logger.info(
            "Intent detected: UNKNOWN"
        )

        return "UNKNOWN"

    @staticmethod
    def show_intent(text):

        intent = IntentClassifier.classify(
            text
        )

        print("\nIntent Classification:")

        print(intent)