from logs.logger import logger


class HealthMonitor:

    def __init__(self):

        self.health = {

            "cpu": "NORMAL",

            "memory": "NORMAL",

            "disk": "NORMAL",

            "providers": "ONLINE",

            "brain_modules": "HEALTHY",

            "voice_system": "READY",

            "world_model": "HEALTHY",

            "overall_status": "GOOD"

        }

    def update(
            self,
            component,
            state):

        self.health[component] = state

        logger.info(
            f"Health updated: {component}"
        )

        self.evaluate()

    def evaluate(self):

        if any(

                state in [

                    "CRITICAL",

                    "OFFLINE",

                    "FAILED"

                ]

                for state in self.health.values()

        ):

            self.health[
                "overall_status"
            ] = "CRITICAL"

        elif any(

                state in [

                    "WARNING",

                    "DEGRADED"

                ]

                for state in self.health.values()

        ):

            self.health[
                "overall_status"
            ] = "WARNING"

        else:

            self.health[
                "overall_status"
            ] = "GOOD"

    def show_health(self):

        print("\nSystem Health:\n")

        for component, state in self.health.items():

            print(
                f"{component}: {state}"
            )