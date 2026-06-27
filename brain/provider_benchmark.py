from brain.provider_memory import ProviderMemory
from logs.logger import logger


class ProviderBenchmark:

    @staticmethod
    def rank_providers(task_type=None):

        records = ProviderMemory.get_all()

        scores = {}

        for record in records:

            if task_type and record["task_type"] != task_type:

                continue

            provider = record["provider"]

            if provider not in scores:

                scores[provider] = {
                    "success": 0,
                    "failure": 0,
                    "score": 0
                }

            if record["result"] == "SUCCESS":

                scores[provider]["success"] += 1

                scores[provider]["score"] += 1

            elif record["result"] == "FAILURE":

                scores[provider]["failure"] += 1

                scores[provider]["score"] -= 1

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1]["score"],
            reverse=True
        )

        logger.info(
            "Provider benchmark ranking generated."
        )

        return ranked

    @staticmethod
    def show_ranking(task_type=None):

        ranked = ProviderBenchmark.rank_providers(
            task_type
        )

        print("\nProvider Benchmark Ranking:")

        if task_type:

            print(
                f"Task Type: {task_type}"
            )

        if not ranked:

            print("No provider benchmark data found.")

        else:

            for index, item in enumerate(
                    ranked,
                    start=1):

                provider = item[0]

                data = item[1]

                print(
                    f"{index}. {provider} | "
                    f"Score={data['score']} | "
                    f"Success={data['success']} | "
                    f"Failure={data['failure']}"
                )