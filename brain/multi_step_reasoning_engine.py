from logs.logger import logger


class MultiStepReasoningEngine:

    def __init__(self):

        self.reasoning_chains = {}

    def create_chain(
            self,
            problem,
            steps):

        self.reasoning_chains[
            problem
        ] = steps

        logger.info(
            f"Reasoning chain created: "
            f"{problem}"
        )

    def show_chain(
            self,
            problem):

        print(
            f"\nReasoning Chain: {problem}\n"
        )

        steps = self.reasoning_chains.get(
            problem,
            []
        )

        if not steps:

            print(
                "No reasoning chain found."
            )

            return

        for index, step in enumerate(
                steps,
                start=1):

            print(
                f"{index}. {step}"
            )