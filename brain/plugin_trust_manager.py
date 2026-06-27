from logs.logger import logger


class PluginTrustManager:

    DANGEROUS_PERMISSIONS = [
        "delete_file",
        "format_disk",
        "access_secrets",
        "execute_system_command"
    ]

    @staticmethod
    def evaluate_plugin(plugin_info):

        trust_score = plugin_info.get(
            "trust_score",
            0
        )

        permissions = plugin_info.get(
            "permissions",
            []
        )

        status = plugin_info.get(
            "status",
            "UNKNOWN"
        )

        dangerous_found = []

        for permission in permissions:

            if permission in PluginTrustManager.DANGEROUS_PERMISSIONS:

                dangerous_found.append(
                    permission
                )

        if status == "BLOCKED":

            decision = "BLOCKED"

        elif dangerous_found:

            decision = "BLOCKED"

        elif trust_score >= 75:

            decision = "TRUSTED"

        elif trust_score >= 40:

            decision = "REVIEW_REQUIRED"

        else:

            decision = "BLOCKED"

        logger.info(
            f"Plugin trust decision: {decision}"
        )

        return {
            "decision": decision,
            "dangerous_permissions": dangerous_found,
            "trust_score": trust_score,
            "status": status
        }

    @staticmethod
    def show_decision(plugin_info):

        result = PluginTrustManager.evaluate_plugin(
            plugin_info
        )

        print("\nPlugin Trust Manager:\n")

        print(
            f"Trust Score: {result['trust_score']}"
        )

        print(
            f"Status: {result['status']}"
        )

        print(
            f"Dangerous Permissions: {result['dangerous_permissions']}"
        )

        print(
            f"Decision: {result['decision']}"
        )