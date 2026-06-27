from logs.logger import logger


class ConsensusEngine:

    def __init__(self):

        self.votes = {}

    def vote(
            self,
            topic,
            agent,
            choice):

        if topic not in self.votes:

            self.votes[topic] = []

        self.votes[topic].append(
            {
                "agent": agent,
                "choice": choice
            }
        )

        logger.info(
            f"Vote recorded: "
            f"{agent}"
        )

    def get_consensus(
            self,
            topic):

        if topic not in self.votes:

            return None

        counts = {}

        for vote in self.votes[topic]:

            choice = vote["choice"]

            counts[choice] = (
                counts.get(
                    choice,
                    0
                ) + 1
            )

        return max(
            counts,
            key=counts.get
        )

    def show_votes(self):

        print(
            "\nConsensus Engine:\n"
        )

        for topic, votes in (
                self.votes.items()):

            print(
                f"Topic: {topic}"
            )

            for vote in votes:

                print(
                    f"{vote['agent']} -> "
                    f"{vote['choice']}"
                )

            print(
                f"Consensus: "
                f"{self.get_consensus(topic)}"
            )

            print()