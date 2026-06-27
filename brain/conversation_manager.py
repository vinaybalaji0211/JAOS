from logs.logger import logger


class ConversationManager:

    def __init__(self):

        self.active = False
        self.history = []

    def start(self):

        self.active = True

        logger.info(
            "Conversation started."
        )

    def add_message(
            self,
            speaker,
            message):

        self.history.append(
            {
                "speaker": speaker,
                "message": message
            }
        )

        logger.info(
            f"Message added: {speaker}"
        )

    def end(self):

        self.active = False

        logger.info(
            "Conversation ended."
        )

    def show_history(self):

        print(
            "\nConversation Manager:\n"
        )

        print(
            f"Active: {self.active}\n"
        )

        for item in self.history:

            print(
                f"{item['speaker']}: "
                f"{item['message']}"
            )