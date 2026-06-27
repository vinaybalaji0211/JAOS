from logs.logger import logger


class AgentReputationSystem:

    def __init__(self):

        self.reputation_scores = {}

    def register_agent(
            self,
            agent_name,
            score=50):

        self.reputation_scores[
            agent_name
        ] = score

        logger.info(
            f"Agent reputation created: "
            f"{agent_name}"
        )

    def increase_score(
            self,
            agent_name,
            amount):

        if agent_name in self.reputation_scores:

            self.reputation_scores[
                agent_name
            ] += amount

    def decrease_score(
            self,
            agent_name,
            amount):

        if agent_name in self.reputation_scores:

            self.reputation_scores[
                agent_name
            ] -= amount

    def get_score(
            self,
            agent_name):

        return self.reputation_scores.get(
            agent_name
        )

    def show_reputation(self):

        print(
            "\nAgent Reputation System:\n"
        )

        if not self.reputation_scores:

            print(
                "No agents tracked."
            )

            return

        for agent, score in (
                self.reputation_scores.items()):

            print(
                f"Agent: {agent}"
            )

            print(
                f"Score: {score}"
            )

            print()