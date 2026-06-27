from logs.logger import logger


class KnowledgeValidationEngine:

    def __init__(self):

        self.records = []

    def validate(
            self,
            source,
            topic,
            trust_score):

        status = (
            "ACCEPTED"
            if trust_score >= 70
            else "REVIEW"
        )

        record = {
            "source": source,
            "topic": topic,
            "trust_score": trust_score,
            "status": status
        }

        self.records.append(record)

        logger.info(
            f"Knowledge validated: {topic}"
        )

        return status

    def show_records(self):

        print(
            "\nKnowledge Validation Engine:\n"
        )

        if not self.records:

            print("No validation records.")
            return

        for record in self.records:

            print(
                f"Source: {record['source']}"
            )

            print(
                f"Topic: {record['topic']}"
            )

            print(
                f"Trust Score: "
                f"{record['trust_score']}"
            )

            print(
                f"Status: "
                f"{record['status']}"
            )

            print()