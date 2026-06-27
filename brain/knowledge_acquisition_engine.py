from logs.logger import logger


class KnowledgeAcquisitionEngine:

    def __init__(self):

        self.learning_targets = []

    def acquire_subject(
            self,
            subject,
            domain="GENERAL"):

        record = {
            "subject": subject,
            "domain": domain,
            "status": "LEARNING"
        }

        self.learning_targets.append(
            record
        )

        logger.info(
            f"Learning initiated: {subject}"
        )

    def complete_subject(
            self,
            subject):

        for item in self.learning_targets:

            if item["subject"] == subject:

                item["status"] = "LEARNED"

                logger.info(
                    f"Learning completed: {subject}"
                )

    def show_learning_targets(self):

        print(
            "\nKnowledge Acquisition Engine:\n"
        )

        if not self.learning_targets:

            print(
                "No learning targets."
            )

            return

        for item in self.learning_targets:

            print(
                f"{item['subject']} | "
                f"{item['domain']} | "
                f"{item['status']}"
            )