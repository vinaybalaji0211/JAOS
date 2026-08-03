from collections import Counter

from logs.logger import logger


class PatternDiscoveryEngine:

    @staticmethod
    def discover(items):

        counts = Counter(items)

        patterns = []

        for item, count in counts.items():

            if count > 1:

                patterns.append(

                    {
                        "pattern": item,

                        "occurrences": count
                    }

                )

        logger.info(
            "Pattern discovery completed."
        )

        return patterns

    @staticmethod
    def show_patterns(items):

        patterns = (
            PatternDiscoveryEngine.discover(
                items
            )
        )

        print("\nPattern Discovery:\n")

        if not patterns:

            print(
                "No significant patterns detected."
            )

            return

        for index, pattern in enumerate(
                patterns,
                start=1):

            print(
                f"{index}. "
                f"{pattern['pattern']} "
                f"({pattern['occurrences']} occurrences)"
            )