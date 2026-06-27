from logs.logger import logger


class DevelopmentWorkspaceManager:

    def __init__(self):

        self.workspaces = {}

    def register_workspace(
            self,
            name,
            repository,
            vscode_workspace):

        self.workspaces[name] = {
            "repository": repository,
            "vscode_workspace": vscode_workspace
        }

        logger.info(
            f"Development workspace registered: {name}"
        )

    def show_workspaces(self):

        print("\n=== Development Workspace Manager ===\n")

        if not self.workspaces:

            print("No development workspaces.")
            return

        for name, data in self.workspaces.items():

            print(name)
            print(f"  Repository : {data['repository']}")
            print(f"  VS Code    : {data['vscode_workspace']}")
            print()