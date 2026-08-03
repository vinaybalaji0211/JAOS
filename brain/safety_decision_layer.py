from logs.logger import logger


class SafetyDecisionLayer:

    @staticmethod
    def decide(
            risk_level,
            confidence,
            conflict_count,
            feasible,
            resources_ok):

        if risk_level == "BLOCKED" or (
                confidence < 40
                or conflict_count >= 3
                or not feasible):

            decision = "BLOCK"

        elif (
                risk_level == "HIGH"
                or confidence < 60
                or not resources_ok):

            decision = "RESTRICT"

        elif (
                risk_level == "MEDIUM"
                or confidence < 80
                or conflict_count > 0):

            decision = "WARNING"

        else:

            decision = "ALLOW"

        logger.info(
            f"Safety decision: {decision}"
        )

        return decision

    @staticmethod
    def explain(
            risk_level,
            confidence,
            conflict_count,
            feasible,
            resources_ok):

        decision = SafetyDecisionLayer.decide(
            risk_level,
            confidence,
            conflict_count,
            feasible,
            resources_ok
        )

        print("\nSafety Report:\n")

        print(
            f"Risk Level: {risk_level}"
        )

        print(
            f"Confidence: {confidence}"
        )

        print(
            f"Conflicts: {conflict_count}"
        )

        print(
            f"Feasible: {feasible}"
        )

        print(
            f"Resources OK: {resources_ok}"
        )

        print(
            f"\nDecision: {decision}"
        )