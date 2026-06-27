from logs.logger import logger


class ToolPermissionManager:

    def __init__(self):

        self.permissions = {}

    def register_tool(
            self,
            tool_name,
            approval_required):

        self.permissions[
            tool_name
        ] = {
            "approval_required":
            approval_required
        }

        logger.info(
            f"Permission registered: "
            f"{tool_name}"
        )

    def requires_approval(
            self,
            tool_name):

        tool = self.permissions.get(
            tool_name
        )

        if not tool:

            return True

        return tool[
            "approval_required"
        ]

    def show_permissions(self):

        print(
            "\nTool Permission Manager:\n"
        )

        if not self.permissions:

            print(
                "No permissions."
            )

            return

        for tool, info in (
                self.permissions.items()):

            print(
                f"Tool: {tool}"
            )

            print(
                f"Approval Required: "
                f"{info['approval_required']}"
            )

            print()