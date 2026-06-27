from logs.logger import logger


class HypothesisGenerationEngine:

    def __init__(self):

        self.hypotheses = {}

    def generate(
            self,
            problem,
            hypotheses):

        self.hypotheses[
            problem
        ] = hypotheses

        logger.info(
            f"Hypotheses generated: "
            f"{problem}"
        )

    def show_hypotheses(
            self,
            problem):

        print(
            f"\nProblem: {problem}\n"
        )

        items = self.hypotheses.get(
            problem,
            []
        )

        if not items:

            print(
                "No hypotheses."
            )

            return

        for index, hypothesis in enumerate(
                items,
                start=1):

            print(
                f"{index}. {hypothesis}"
            )