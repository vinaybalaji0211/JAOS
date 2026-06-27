from logs.logger import logger


class AgentBlueprintDesigner:

    def __init__(self):

        self.blueprints = {}

    def create_blueprint(
            self,
            agent_name,
            role,
            capabilities,
            permissions,
            dependencies):

        blueprint = {
            "role": role,
            "capabilities": capabilities,
            "permissions": permissions,
            "dependencies": dependencies
        }

        self.blueprints[
            agent_name
        ] = blueprint

        logger.info(
            f"Blueprint created: "
            f"{agent_name}"
        )

    def show_blueprints(self):

        print(
            "\nAgent Blueprint Designer:\n"
        )

        if not self.blueprints:

            print(
                "No blueprints."
            )

            return

        for name, bp in (
                self.blueprints.items()):

            print(
                f"Agent: {name}"
            )

            print(
                f"Role: {bp['role']}"
            )

            print(
                f"Capabilities: "
                f"{bp['capabilities']}"
            )

            print(
                f"Permissions: "
                f"{bp['permissions']}"
            )

            print(
                f"Dependencies: "
                f"{bp['dependencies']}"
            )

            print()