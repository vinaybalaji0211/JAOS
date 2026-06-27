from logs.logger import logger


class ConversationQualityAnalyzer:

    def __init__(self):

        self.successful_responses = 0
        self.misunderstandings = 0

    def record_success(self):

        self.successful_responses += 1

        logger.info(
            "Conversation success recorded."
        )

    def record_misunderstanding(self):

        self.misunderstandings += 1

        logger.info(
            "Conversation misunderstanding recorded."
        )

    def calculate_quality(self):

        total = (
            self.successful_responses +
            self.misunderstandings
        )

        if total == 0:
            return 100

        return round(
            (self.successful_responses / total) * 100,
            2
        )

    def show_report(self):

        print(
            "\nConversation Quality Analyzer:\n"
        )

        print(
            f"Successful Responses: "
            f"{self.successful_responses}"
        )

        print(
            f"Misunderstandings: "
            f"{self.misunderstandings}"
        )

        print(
            f"Quality Score: "
            f"{self.calculate_quality()}%"
        )