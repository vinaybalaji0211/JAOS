from logs.logger import logger


class PlanValidator:

    @staticmethod
    def validate(
            plan,
            matched_capabilities,
            missing_capabilities,
            risk_level,
            execution_strategy):

        issues = []

        if not plan:

            issues.append(
                "Plan is missing."
            )

        elif len(plan) == 0:

            issues.append(
                "Plan has no steps."
            )

        if not matched_capabilities:

            issues.append(
                "No matched capabilities found."
            )

        if missing_capabilities:

            issues.append(
                f"Missing capabilities: {missing_capabilities}"
            )

        if risk_level == "HIGH":

            issues.append(
                "Risk level is high."
            )

        if not execution_strategy:

            issues.append(
                "Execution strategy is missing."
            )

        is_valid = len(issues) == 0

        logger.info(
            f"Plan validation completed. Valid={is_valid}"
        )

        return {
            "valid": is_valid,
            "issues": issues
        }

    @staticmethod
    def show_validation(
            plan,
            matched_capabilities,
            missing_capabilities,
            risk_level,
            execution_strategy):

        result = PlanValidator.validate(
            plan,
            matched_capabilities,
            missing_capabilities,
            risk_level,
            execution_strategy
        )

        print("\nPlan Validation Result:")

        print(
            f"Valid: {result['valid']}"
        )

        if result["issues"]:

            print("\nIssues:")

            for issue in result["issues"]:

                print(
                    f"- {issue}"
                )

        else:

            print("No issues found.")