from logs.logger import logger


class ToolCore:

    def __init__(self):

        self.tools = {}

    def register_tool(
            self,
            tool_name,
            description):

        self.tools[
            tool_name
        ] = description

        logger.info(
            f"Tool registered: "
            f"{tool_name}"
        )

    def get_tool(
            self,
            tool_name):

        return self.tools.get(
            tool_name
        )

    def show_tools(self):

        print(
            "\nTool Core:\n"
        )

        if not self.tools:

            print(
                "No tools registered."
            )

            return

        for tool, description in (
                self.tools.items()):

            print(
                f"Tool: {tool}"
            )

            print(
                f"Description: "
                f"{description}"
            )

            print()