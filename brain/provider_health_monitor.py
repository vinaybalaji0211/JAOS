from logs.logger import logger


class ProviderHealthMonitor:

    def __init__(self):

        self.health_data = {}

    def add_provider(self, provider):

        if provider not in self.health_data:

            self.health_data[provider] = {

                "success_count": 0,

                "failure_count": 0,

                "success_rate": 100.0,

                "latency": 0.0,

                "status": "HEALTHY"

            }

    def record_success(
            self,
            provider,
            latency=0.0):

        self.add_provider(provider)

        self.health_data[provider][
            "success_count"
        ] += 1

        self.health_data[provider][
            "latency"
        ] = latency

        self.update_health(provider)

        logger.info(
            f"{provider} success recorded"
        )

    def record_failure(
            self,
            provider):

        self.add_provider(provider)

        self.health_data[provider][
            "failure_count"
        ] += 1

        self.update_health(provider)

        logger.warning(
            f"{provider} failure recorded"
        )

    def update_health(
            self,
            provider):

        success = self.health_data[
            provider
        ]["success_count"]

        failure = self.health_data[
            provider
        ]["failure_count"]

        total = success + failure

        if total > 0:

            rate = (
                success / total
            ) * 100

            self.health_data[
                provider
            ]["success_rate"] = round(
                rate,
                2
            )

            if rate < 70:

                self.health_data[
                    provider
                ]["status"] = "UNHEALTHY"

            else:

                self.health_data[
                    provider
                ]["status"] = "HEALTHY"

    def show_health(self):

        print("\nProvider Health:\n")

        for provider, data in (
                self.health_data.items()):

            print(

                f"{provider} "

                f"| Success={data['success_count']} "

                f"| Failure={data['failure_count']} "

                f"| Success Rate={data['success_rate']}% "

                f"| Latency={data['latency']} sec "

                f"| Status={data['status']}"

            )