from logs.logger import logger


class SelfAwareness:

    def __init__(self):

        self.identity = {

            "name": "JARVIS",

            "version": "1.0",

            "mode": "24/7 Autonomous AI OS"

        }

        self.state = "ACTIVE"

        self.capabilities = [

            "planning",

            "reasoning",

            "memory",

            "providers",

            "tools",

            "skills",

            "agents"

        ]

        self.weaknesses = [

            "vision",

            "device_control",

            "voice"

        ]

        self.goals = [

            "Become autonomous",

            "Improve capabilities",

            "Maintain safety",

            "Learn continuously"

        ]

    def show_identity(self):

        print("\nIdentity:\n")

        for key, value in self.identity.items():

            print(

                f"{key}: {value}"

            )

    def show_state(self):

        print(

            f"\nCurrent State: {self.state}"

        )

    def show_capabilities(self):

        print("\nCapabilities:\n")

        for capability in self.capabilities:

            print(

                f"- {capability}"

            )

    def show_weaknesses(self):

        print("\nWeaknesses:\n")

        for weakness in self.weaknesses:

            print(

                f"- {weakness}"

            )

    def show_goals(self):

        print("\nLong-Term Goals:\n")

        for goal in self.goals:

            print(

                f"- {goal}"

            )

        logger.info(

            "Self-awareness information displayed."

        )