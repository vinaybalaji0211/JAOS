from collections import Counter
from logs.logger import logger


class FeatureRequestIntelligence:

    def __init__(self):

        self.requests = []

    def add_request(
            self,
            feature):

        self.requests.append(
            feature
        )

        logger.info(
            f"Feature request added: {feature}"
        )

    def show_statistics(self):

        print(
            "\nFeature Request Statistics\n"
        )

        if not self.requests:

            print(
                "No requests."
            )

            return

        counts = Counter(
            self.requests
        )

        for feature, total in (
                counts.items()):

            print(
                f"{feature}: {total}"
            )

    def most_requested(self):

        if not self.requests:

            return None

        counts = Counter(
            self.requests
        )

        return counts.most_common(1)[0]