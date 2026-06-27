from logs.logger import logger


class LearningManager:

    def __init__(self):

        self.memory = {

            "successes": [],

            "failures": [],

            "lessons": [],

            "strategies": [],

            "provider_stats": [],

            "resource_problems": [],

            "user_preferences": [],

            "patterns": []

        }

    def learn(
            self,
            category,
            item):

        if category not in self.memory:

            self.memory[category] = []

        self.memory[category].append(
            item
        )

        logger.info(
            f"Learned {category}: {item}"
        )

    def get(
            self,
            category):

        return self.memory.get(
            category,
            []
        )

    def show_learning(self):

        print("\nLearning Manager:\n")

        for category, items in self.memory.items():

            print(
                f"{category}: {len(items)} items"
            )