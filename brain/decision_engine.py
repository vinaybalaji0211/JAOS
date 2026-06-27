from logs.logger import logger


class DecisionEngine:

    @staticmethod
    def score_option(option):
        score = 0

        score += option.get("priority", 0)
        score += option.get("confidence", 0)
        score += option.get("goal_alignment", 0)

        if option.get("resources_ok", False):
            score += 20

        risk = option.get("risk", "LOW")

        if risk == "LOW":
            score += 20
        elif risk == "MEDIUM":
            score += 5
        elif risk == "HIGH":
            score -= 30
        elif risk == "BLOCKED":
            score -= 100

        return score

    @staticmethod
    def decide(options):
        if not options:
            return None

        scored_options = []

        for option in options:
            scored_options.append(
                {
                    "name": option.get("name"),
                    "score": DecisionEngine.score_option(option),
                    "risk": option.get("risk")
                }
            )

        scored_options.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        best = scored_options[0]

        logger.info(
            f"Decision made: {best['name']}"
        )

        return best

    @staticmethod
    def show_decision(options):
        best = DecisionEngine.decide(options)

        print("\nDecision Engine:\n")

        if not best:
            print("No options available.")
            return

        print(f"Best Option: {best['name']}")
        print(f"Score: {best['score']}")
        print(f"Risk: {best['risk']}")