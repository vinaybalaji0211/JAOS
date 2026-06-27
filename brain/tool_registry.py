from logs.logger import logger


class ToolRegistry:

    def __init__(self):

        self.registry = {}

    def register(
            self,
            tool_name,
            category,
            description):

        self.registry[
            tool_name
        ] = {
            "category": category,
            "description": description
        }

        logger.info(
            f"Tool registered: "
            f"{tool_name}"
        )

    def get_tool(
            self,
            tool_name):

        return self.registry.get(
            tool_name
        )

    def show_registry(self):

        print(
            "\nTool Registry:\n"
        )

        if not self.registry:

            print(
                "No tools registered."
            )

            return

        for tool, info in (
                self.registry.items()):

            print(
                f"Tool: {tool}"
            )

            print(
                f"Category: "
                f"{info['category']}"
            )

            print(
                f"Description: "
                f"{info['description']}"
            )

            print()