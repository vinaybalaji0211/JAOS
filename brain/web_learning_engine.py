from logs.logger import logger


class WebLearningEngine:

    def __init__(self):

        self.learned_content = []

    def learn(
            self,
            website,
            topic):

        record = {
            "website": website,
            "topic": topic
        }

        self.learned_content.append(
            record
        )

        logger.info(
            f"Learned from website: "
            f"{website}"
        )

    def show_learning(self):

        print(
            "\nWeb Learning Engine:\n"
        )

        if not self.learned_content:

            print(
                "No learned content."
            )

            return

        for item in self.learned_content:

            print(
                f"Website: "
                f"{item['website']}"
            )

            print(
                f"Topic: "
                f"{item['topic']}"
            )

            print()