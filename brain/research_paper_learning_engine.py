from logs.logger import logger


class ResearchPaperLearningEngine:

    def __init__(self):

        self.papers = []

    def learn_paper(
            self,
            title,
            topic):

        record = {
            "title": title,
            "topic": topic
        }

        self.papers.append(
            record
        )

        logger.info(
            f"Learned paper: "
            f"{title}"
        )

    def show_papers(self):

        print(
            "\nResearch Paper Learning Engine:\n"
        )

        if not self.papers:

            print(
                "No papers learned."
            )

            return

        for paper in self.papers:

            print(
                f"Title: "
                f"{paper['title']}"
            )

            print(
                f"Topic: "
                f"{paper['topic']}"
            )

            print()