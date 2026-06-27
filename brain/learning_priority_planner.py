from logs.logger import logger


class LearningPriorityPlanner:

    def __init__(self):

        self.priorities = {}

    def set_priority(
            self,
            domain,
            priority):

        self.priorities[domain] = priority

        logger.info(
            f"Priority set: {domain}"
        )

    def get_priority(
            self,
            domain):

        return self.priorities.get(
            domain,
            "UNKNOWN"
        )

    def show_priorities(self):

        print(
            "\nLearning Priority Planner:\n"
        )

        if not self.priorities:

            print(
                "No priorities defined."
            )

            return

        for domain, priority in (
                self.priorities.items()):

            print(
                f"{domain}: {priority}"
            )