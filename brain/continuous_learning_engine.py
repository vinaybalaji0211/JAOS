from logs.logger import logger


class ContinuousLearningEngine:

    def __init__(self):

        self.learned_topics = []

    def learn(
            self,
            topic):

        self.learned_topics.append(
            topic
        )

        logger.info(
            f"Learned topic: {topic}"
        )

    def has_learned(
            self,
            topic):

        return topic in self.learned_topics

    def show_progress(self):

        print(
            "\nContinuous Learning Engine:\n"
        )

        if not self.learned_topics:

            print(
                "No topics learned."
            )

            return

        for index, topic in enumerate(
                self.learned_topics,
                start=1):

            print(
                f"{index}. {topic}"
            )