from logs.logger import logger


class HiddenRequirementDetector:

    REQUIRED_KEYWORDS = {
        "app": [
            "platform",
            "features",
            "users"
        ],
        "automation": [
            "trigger",
            "action",
            "permission"
        ],
        "ai": [
            "provider",
            "model",
            "data"
        ],
        "file": [
            "path",
            "operation"
        ]
    }

    @staticmethod
    def detect(goal):

        missing = []

        goal_lower = goal.lower()

        for category, requirements in HiddenRequirementDetector.REQUIRED_KEYWORDS.items():

            if category in goal_lower:

                for requirement in requirements:

                    if requirement not in goal_lower:

                        missing.append(requirement)

        logger.info(
            f"Hidden requirements detected: {missing}"
        )

        return missing

    @staticmethod
    def show_missing(goal):

        missing = HiddenRequirementDetector.detect(
            goal
        )

        print("\nHidden Requirement Check:")

        if not missing:

            print("No hidden requirements detected.")

        else:

            print("Missing requirements:")

            for item in missing:

                print(f"- {item}")