from logs.logger import logger


class KnowledgeGapDetector:

    def __init__(self):

        self.knowledge_scores = {}

    def record_score(
            self,
            area,
            score):

        self.knowledge_scores[
            area
        ] = score

        logger.info(
            f"Knowledge score recorded for {area}"
        )

    def detect_gaps(
            self,
            threshold=75):

        gaps = []

        for area, score in self.knowledge_scores.items():

            if score < threshold:

                gaps.append(
                    {
                        "area": area,
                        "score": score
                    }
                )

        return gaps

    def show_gaps(
            self,
            threshold=75):

        gaps = self.detect_gaps(
            threshold
        )

        print(
            "\nKnowledge Gap Detector:\n"
        )

        if not gaps:

            print(
                "No knowledge gaps detected."
            )

            return

        for gap in gaps:

            print(
                f"{gap['area']} | "
                f"Score: {gap['score']}"
            )