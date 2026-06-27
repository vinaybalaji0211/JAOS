from logs.logger import logger


class ProviderPerformanceLearning:

    def __init__(self):

        self.providers = {}

    def record(
            self,
            provider,
            task_type,
            success=True):

        key = (
            provider,
            task_type
        )

        if key not in self.providers:

            self.providers[key] = {

                "successes": 0,

                "failures": 0

            }

        if success:

            self.providers[key]["successes"] += 1

        else:

            self.providers[key]["failures"] += 1

        logger.info(
            f"Recorded performance for {provider}"
        )

    def best_provider(
            self,
            task_type):

        best = None

        best_rate = -1

        for (
                provider,
                task), stats in self.providers.items():

            if task != task_type:

                continue

            total = (
                stats["successes"]
                + stats["failures"]
            )

            if total == 0:

                continue

            rate = (
                stats["successes"]
                / total
            )

            if rate > best_rate:

                best_rate = rate

                best = provider

        return best

    def show_stats(self):

        print("\nProvider Performance:\n")

        for (
                provider,
                task), stats in self.providers.items():

            total = (
                stats["successes"]
                + stats["failures"]
            )

            rate = round(
                stats["successes"]
                * 100
                / total,
                2
            )

            print(
                f"{provider} | "
                f"{task} | "
                f"{rate}% success"
            )