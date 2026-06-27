from logs.logger import logger


class MemoryImportanceEngine:

    @staticmethod
    def evaluate(
            memory_text,
            category="GENERAL"):

        text = memory_text.lower()

        score = 0

        important_keywords = [
            "security",
            "roadmap",
            "cloud",
            "author",
            "preference",
            "goal",
            "agent",
            "memory",
            "jarvis"
        ]

        for keyword in important_keywords:

            if keyword in text:

                score += 15

        if category in [
            "SECURITY",
            "ROADMAP",
            "MEMORY",
            "AUTHOR",
            "GOAL"
        ]:

            score += 25

        if score >= 70:

            decision = "STORE_HIGH_PRIORITY"

        elif score >= 35:

            decision = "STORE_NORMAL"

        else:

            decision = "IGNORE_OR_SHORT_TERM"

        logger.info(
            f"Memory importance decision: {decision}"
        )

        return {
            "score": score,
            "decision": decision
        }

    @staticmethod
    def show_evaluation(
            memory_text,
            category="GENERAL"):

        result = MemoryImportanceEngine.evaluate(
            memory_text,
            category
        )

        print("\nMemory Importance Engine:\n")

        print(
            f"Memory: {memory_text}"
        )

        print(
            f"Category: {category}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Decision: {result['decision']}"
        )