from logs.logger import logger


class CapabilityRestrictions:

    CAPABILITIES = {

        "READ_MEMORY": "BASIC",

        "RUN_DIAGNOSTICS": "BASIC",

        "VIEW_LOGS": "BASIC",

        "INSTALL_PACKAGE": "EXTENDED",

        "EDIT_CONFIG": "EXTENDED",

        "START_BACKGROUND_TASK": "EXTENDED",

        "DELETE_FILE": "RESTRICTED",

        "FORMAT_DISK": "RESTRICTED",

        "ACCESS_SECRETS": "RESTRICTED"

    }

    @staticmethod
    def get_level(
            action):

        level = (

            CapabilityRestrictions
            .CAPABILITIES
            .get(

                action,

                "UNKNOWN"

            )

        )

        logger.info(
            f"Capability check: {action}"
        )

        return level

    @staticmethod
    def show_level(
            action):

        level = (
            CapabilityRestrictions
            .get_level(
                action
            )
        )

        print("\nCapability Restrictions:\n")

        print(
            f"Action: {action}"
        )

        print(
            f"Capability Level: {level}"
        )