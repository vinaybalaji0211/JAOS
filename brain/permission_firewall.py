from logs.logger import logger


class PermissionFirewall:

    RULES = {

        "READ_MEMORY":
            "ALLOW",

        "RUN_DIAGNOSTICS":
            "ALLOW",

        "INSTALL_PACKAGE":
            "REQUIRE_APPROVAL",

        "EDIT_CONFIG":
            "REQUIRE_APPROVAL",

        "DELETE_FILE":
            "BLOCK",

        "FORMAT_DISK":
            "BLOCK"

    }

    @staticmethod
    def evaluate(
            action):

        decision = (
            PermissionFirewall
            .RULES
            .get(

                action,

                "REQUIRE_APPROVAL"

            )
        )

        logger.info(
            f"Firewall decision: {action} -> {decision}"
        )

        return decision

    @staticmethod
    def show_decision(
            action):

        decision = (
            PermissionFirewall
            .evaluate(
                action
            )
        )

        print("\nPermission Firewall:\n")

        print(
            f"Action: {action}"
        )

        print(
            f"Decision: {decision}"
        )