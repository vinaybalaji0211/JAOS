from logs.logger import logger


class PluginRegistry:

    def __init__(self):

        self.plugins = {}

    def register_plugin(
            self,
            name,
            version,
            author,
            capabilities=None,
            dependencies=None,
            permissions=None,
            trust_score=50):

        if capabilities is None:
            capabilities = []

        if dependencies is None:
            dependencies = []

        if permissions is None:
            permissions = []

        self.plugins[name] = {
            "version": version,
            "author": author,
            "status": "REGISTERED",
            "trust_score": trust_score,
            "capabilities": capabilities,
            "dependencies": dependencies,
            "permissions": permissions
        }

        logger.info(
            f"Plugin registered: {name}"
        )

    def update_status(
            self,
            name,
            status):

        if name in self.plugins:

            self.plugins[name]["status"] = status

            logger.info(
                f"Plugin status updated: {name}"
            )

    def get_plugin(
            self,
            name):

        return self.plugins.get(name)

    def show_plugins(self):

        print("\nPlugin Registry:\n")

        if not self.plugins:

            print("No plugins registered.")

            return

        for name, details in self.plugins.items():

            print(f"Name: {name}")
            print(f"Version: {details['version']}")
            print(f"Author: {details['author']}")
            print(f"Status: {details['status']}")
            print(f"Trust Score: {details['trust_score']}")
            print(f"Capabilities: {details['capabilities']}")
            print(f"Dependencies: {details['dependencies']}")
            print(f"Permissions: {details['permissions']}")
            print()