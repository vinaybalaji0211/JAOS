from logs.logger import logger


class ConversationContextTracker:

    def __init__(self):

        self.current_topic = None
        self.previous_topic = None
        self.history = []

    def change_topic(self, topic):

        self.previous_topic = self.current_topic
        self.current_topic = topic

        self.history.append(topic)

        logger.info(
            f"Topic changed to {topic}"
        )

    def show_context(self):

        print(
            "\nConversation Context Tracker:\n"
        )

        print(
            f"Current Topic: "
            f"{self.current_topic}"
        )

        print(
            f"Previous Topic: "
            f"{self.previous_topic}"
        )

        print(
            f"History: "
            f"{self.history}"
        )