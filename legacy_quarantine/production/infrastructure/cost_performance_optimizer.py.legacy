from logs.logger import logger


class CostPerformanceOptimizer:

    def __init__(self):

        self.resources = {}

    def register_resource(
            self,
            name,
            estimated_cost,
            estimated_speed):

        self.resources[name] = {
            "cost": estimated_cost,
            "speed": estimated_speed
        }

        logger.info(
            f"Resource evaluated: {name}"
        )

    def recommend(self):

        if not self.resources:

            return None

        best = min(
            self.resources.items(),
            key=lambda item: (
                item[1]["cost"],
                -item[1]["speed"]
            )
        )

        return best

    def show_resources(self):

        print("\n=== Cost & Performance ===\n")

        if not self.resources:

            print("No resources.")
            return

        for name, data in self.resources.items():

            print(name)

            print(
                f"  Cost : {data['cost']}"
            )

            print(
                f"  Speed: {data['speed']}"
            )

            print()