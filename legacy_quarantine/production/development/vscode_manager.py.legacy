from logs.logger import logger


class VSCodeManager:

    def __init__(self):

        self.workspaces = {}

    def register_workspace(
            self,
            workspace_name,
            repository):

        self.workspaces[workspace_name] = {
            "repository": repository
        }

        logger.info(
            f"Workspace registered: {workspace_name}"
        )

    def show_workspaces(self):

        print("\n=== VS Code Manager ===\n")

        if not self.workspaces:

            print("No workspaces.")
            return

        for name, data in self.workspaces.items():

            print(name)
            print(
                f"  Repository : {data['repository']}"
            )
            print()