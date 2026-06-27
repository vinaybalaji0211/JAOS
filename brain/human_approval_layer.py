from logs.logger import logger


class HumanApprovalLayer:

    @staticmethod
    def request(
            action,
            decision):

        if decision == "ALLOW":

            result = "APPROVED"

        elif decision == "REQUIRE_APPROVAL":

            result = "WAITING_APPROVAL"

        else:

            result = "DENIED"

        logger.info(
            f"Approval result: {action} -> {result}"
        )

        return result

    @staticmethod
    def show_request(
            action,
            decision):

        result = (
            HumanApprovalLayer.request(
                action,
                decision
            )
        )

        print("\nHuman Approval Layer:\n")

        print(
            f"Action: {action}"
        )

        print(
            f"Result: {result}"
        )