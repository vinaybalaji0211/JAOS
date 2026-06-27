from logs.logger import logger


class ToolRoutingEngine:

    def __init__(self):

        self.routes = {}

    def register_route(
            self,
            task_type,
            tool_name):

        self.routes[
            task_type
        ] = tool_name

        logger.info(
            f"Route registered: "
            f"{task_type}"
        )

    def get_tool(
            self,
            task_type):

        return self.routes.get(
            task_type
        )

    def show_routes(self):

        print(
            "\nTool Routing Engine:\n"
        )

        if not self.routes:

            print(
                "No routes."
            )

            return

        for task, tool in (
                self.routes.items()):

            print(
                f"Task: {task}"
            )

            print(
                f"Tool: {tool}"
            )

            print()