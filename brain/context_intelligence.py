from logs.logger import logger


class ContextIntelligence:

    @staticmethod
    def analyze(context):

        if not context:

            result = "No context available."

        elif "current_goal" in context:

            result = f"Current goal detected: {context['current_goal']}"

        elif "current_phase" in context:

            result = f"Current phase detected: {context['current_phase']}"

        else:

            result = "General context detected."

        logger.info(
            f"Context analyzed: {result}"
        )

        return result