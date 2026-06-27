from logs.logger import logger


class CognitiveState:

    def __init__(self):

        self.state = {

            "mode": "ACTIVE",

            "current_goal":
                "Build Independent 24/7 AI Operating System",

            "current_task":
                None,

            "health":
                "GOOD",

            "confidence":
                100,

            "safety":
                "ALLOW",

            "resource_state":
                "NORMAL",

            "time_period":
                "UNKNOWN",

            "meta_state":
                "LEARNING"

        }

    def update(
            self,
            key,
            value):

        self.state[key] = value

        logger.info(
            f"Cognitive state updated: {key}"
        )

    def get(
            self,
            key):

        return self.state.get(key)

    def show_state(self):

        print("\nCognitive State:\n")

        for key, value in self.state.items():

            print(
                f"{key}: {value}"
            )