from logs.logger import logger


class KnowledgeGapMapper:

    def __init__(self):

        self.required_topics = {}

        self.known_topics = {}

    def define_domain(
            self,
            domain,
            topics):

        self.required_topics[
            domain
        ] = topics

    def add_known_topic(
            self,
            domain,
            topic):

        if domain not in self.known_topics:

            self.known_topics[
                domain
            ] = []

        self.known_topics[
            domain
        ].append(
            topic
        )

    def find_gaps(
            self,
            domain):

        required = self.required_topics.get(
            domain,
            []
        )

        known = self.known_topics.get(
            domain,
            []
        )

        gaps = []

        for topic in required:

            if topic not in known:

                gaps.append(
                    topic
                )

        return gaps

    def show_gaps(
            self,
            domain):

        gaps = self.find_gaps(
            domain
        )

        print(
            f"\nKnowledge Gaps: {domain}\n"
        )

        if not gaps:

            print(
                "No gaps detected."
            )

            return

        for gap in gaps:

            print(
                f"- {gap}"
            )