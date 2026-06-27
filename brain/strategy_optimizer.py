from logs.logger import logger


class StrategyOptimizer:

    @staticmethod
    def optimize(
            success_count,
            failure_count,
            confidence,
            resource_issue=False):

        if resource_issue:

            decision = "MODIFY_STRATEGY"

        elif failure_count > success_count:

            decision = "AVOID_STRATEGY"

        elif success_count > failure_count and confidence >= 80:

            decision = "REUSE_STRATEGY"

        else:

            decision = "TRY_NEW_STRATEGY"

        logger.info(
            f"Strategy optimization decision: {decision}"
        )

        return decision

    @staticmethod
    def show_decision(
            success_count,
            failure_count,
            confidence,
            resource_issue=False):

        decision = StrategyOptimizer.optimize(
            success_count,
            failure_count,
            confidence,
            resource_issue
        )

        print("\nStrategy Optimization:")

        print(
            f"Success Count: {success_count}"
        )

        print(
            f"Failure Count: {failure_count}"
        )

        print(
            f"Confidence: {confidence}"
        )

        print(
            f"Resource Issue: {resource_issue}"
        )

        print(
            f"Decision: {decision}"
        )