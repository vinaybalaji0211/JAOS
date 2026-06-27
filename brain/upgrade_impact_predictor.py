from logs.logger import logger


class UpgradeImpactPredictor:

    def __init__(self):

        self.predictions = []

    def predict(
            self,
            upgrade_name,
            benefits,
            risks,
            complexity):

        prediction = {
            "upgrade": upgrade_name,
            "benefits": benefits,
            "risks": risks,
            "complexity": complexity
        }

        self.predictions.append(
            prediction
        )

        logger.info(
            f"Impact predicted: {upgrade_name}"
        )

    def show_predictions(self):

        print(
            "\nUpgrade Impact Predictor:\n"
        )

        if not self.predictions:

            print(
                "No predictions."
            )

            return

        for item in self.predictions:

            print(
                f"Upgrade: {item['upgrade']}"
            )

            print(
                f"Benefits: {item['benefits']}"
            )

            print(
                f"Risks: {item['risks']}"
            )

            print(
                f"Complexity: "
                f"{item['complexity']}"
            )

            print()