from logs.logger import logger


class EmbodiedLearningEngine:

    def __init__(self):

        self.learning_records = []

    def learn(
            self,
            source,
            lesson):

        self.learning_records.append(
            {
                "source": source,
                "lesson": lesson
            }
        )

        logger.info(
            f"Learning captured from {source}"
        )

    def show_learning(self):

        print(
            "\nEmbodied Learning Engine:\n"
        )

        if not self.learning_records:

            print(
                "No learning records."
            )

            return

        for index, record in enumerate(
                self.learning_records,
                start=1):

            print(
                f"{index}. "
                f"[{record['source']}] "
                f"{record['lesson']}"
            )