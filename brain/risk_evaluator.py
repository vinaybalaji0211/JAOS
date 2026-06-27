from logs.logger import logger


class RiskEvaluator:

    RISK_RULES = {
        "delete_file": "HIGH",
        "system_command": "HIGH",
        "device_control": "HIGH",
        "web_access": "MEDIUM",
        "automation": "MEDIUM",
        "provider_usage": "LOW",
        "memory_change": "LOW",
        "read_file": "LOW",
        "write_file": "MEDIUM"
    }

    @staticmethod
    def evaluate(actions):

        risk_levels = []

        for action in actions:

            risk = RiskEvaluator.RISK_RULES.get(
                action,
                "LOW"
            )

            risk_levels.append(risk)

        if "HIGH" in risk_levels:

            final_risk = "HIGH"

        elif "MEDIUM" in risk_levels:

            final_risk = "MEDIUM"

        else:

            final_risk = "LOW"

        logger.info(
            f"Risk evaluated: {final_risk}"
        )

        return final_risk

    @staticmethod
    def show_risk(actions):

        risk = RiskEvaluator.evaluate(
            actions
        )

        print("\nRisk Evaluation:")

        print(
            f"Actions: {actions}"
        )

        print(
            f"Risk Level: {risk}"
        )