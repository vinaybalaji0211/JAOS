from logs.logger import logger


class ProactiveSuggestions:

    SUGGESTIONS = {

        "memory": (
            "Consider cleaning low-priority memories."
        ),

        "phase": (
            "Remember to perform integration tests."
        ),

        "goal": (
            "Review active goals and priorities."
        ),

        "error": (
            "Check logs and diagnostics."
        ),

        "behavior": (
            "Analyze repeated user patterns."
        )

    }

    @staticmethod
    def suggest(context):

        context = context.lower()

        suggestions = []

        for keyword, message in (
                ProactiveSuggestions
                .SUGGESTIONS.items()):

            if keyword in context:

                suggestions.append(
                    message
                )

        logger.info(
            "Proactive suggestions generated."
        )

        return suggestions

    @staticmethod
    def show_suggestions(context):

        suggestions = (
            ProactiveSuggestions
            .suggest(context)
        )

        print(
            "\nProactive Suggestions:"
        )

        if not suggestions:

            print(
                "No suggestions available."
            )

        else:

            for index, item in enumerate(
                    suggestions,
                    start=1):

                print(
                    f"{index}. {item}"
                )