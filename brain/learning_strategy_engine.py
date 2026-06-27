from logs.logger import logger


class LearningStrategyEngine:

    @staticmethod
    def create_strategy(
            recommendations,
            priority_focus="balanced"):

        strategy = {
            "priority_focus": priority_focus,
            "actions": []
        }

        for item in recommendations:
            if "Threat" in item or "security" in item.lower():
                strategy["actions"].append(
                    f"Security priority: {item}"
                )

            elif "Planning" in item or "planning" in item.lower():
                strategy["actions"].append(
                    f"Planning priority: {item}"
                )

            elif "Recovery" in item or "recovery" in item.lower():
                strategy["actions"].append(
                    f"Recovery priority: {item}"
                )

            else:
                strategy["actions"].append(
                    f"General improvement: {item}"
                )

        logger.info(
            "Learning strategy generated."
        )

        return strategy

    @staticmethod
    def show_strategy(
            recommendations,
            priority_focus="balanced"):

        strategy = LearningStrategyEngine.create_strategy(
            recommendations,
            priority_focus
        )

        print("\nLearning Strategy Engine:\n")

        print(
            f"Priority Focus: {strategy['priority_focus']}"
        )

        print("\nActions:")

        for index, action in enumerate(
                strategy["actions"],
                start=1):

            print(
                f"{index}. {action}"
            )