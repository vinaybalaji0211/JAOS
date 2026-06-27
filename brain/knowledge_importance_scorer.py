from logs.logger import logger


class KnowledgeImportanceScorer:

    HIGH_VALUE_KEYWORDS = [
        "security",
        "cloud",
        "knowledge",
        "agent",
        "memory",
        "physics",
        "learning",
        "jarvis",
        "roadmap"
    ]

    @staticmethod
    def score(
            knowledge_text):

        text = knowledge_text.lower()

        score = 0

        for keyword in (
                KnowledgeImportanceScorer
                .HIGH_VALUE_KEYWORDS):

            if keyword in text:

                score += 15

        if score >= 60:

            priority = "HIGH"

        elif score >= 30:

            priority = "MEDIUM"

        else:

            priority = "LOW"

        logger.info(
            f"Knowledge score: {score}"
        )

        return {
            "score": score,
            "priority": priority
        }

    @staticmethod
    def show_score(
            knowledge_text):

        result = (
            KnowledgeImportanceScorer
            .score(
                knowledge_text
            )
        )

        print(
            "\nKnowledge Importance Scorer:\n"
        )

        print(
            f"Knowledge: {knowledge_text}"
        )

        print(
            f"Score: {result['score']}"
        )

        print(
            f"Priority: "
            f"{result['priority']}"
        )