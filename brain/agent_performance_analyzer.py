from logs.logger import logger


class AgentPerformanceAnalyzer:

    def __init__(self):

        self.agent_metrics = {}

    def register_agent(
            self,
            agent_name):

        self.agent_metrics[agent_name] = {
            "tasks_completed": 0,
            "successes": 0,
            "failures": 0
        }

    def record_success(
            self,
            agent_name):

        if agent_name in self.agent_metrics:

            self.agent_metrics[
                agent_name
            ]["tasks_completed"] += 1

            self.agent_metrics[
                agent_name
            ]["successes"] += 1

            logger.info(
                f"Success recorded for {agent_name}"
            )

    def record_failure(
            self,
            agent_name):

        if agent_name in self.agent_metrics:

            self.agent_metrics[
                agent_name
            ]["tasks_completed"] += 1

            self.agent_metrics[
                agent_name
            ]["failures"] += 1

            logger.info(
                f"Failure recorded for {agent_name}"
            )

    def calculate_score(
            self,
            agent_name):

        if agent_name not in self.agent_metrics:
            return 0

        data = self.agent_metrics[
            agent_name
        ]

        total = data["tasks_completed"]

        if total == 0:
            return 100

        return round(
            (
                data["successes"] /
                total
            ) * 100,
            2
        )

    def show_report(self):

        print(
            "\nAgent Performance Analyzer:\n"
        )

        if not self.agent_metrics:

            print(
                "No agents tracked."
            )

            return

        for agent, data in (
                self.agent_metrics.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                f"Tasks Completed: "
                f"{data['tasks_completed']}"
            )

            print(
                f"Successes: "
                f"{data['successes']}"
            )

            print(
                f"Failures: "
                f"{data['failures']}"
            )

            print(
                f"Score: "
                f"{self.calculate_score(agent)}%"
            )

            print()