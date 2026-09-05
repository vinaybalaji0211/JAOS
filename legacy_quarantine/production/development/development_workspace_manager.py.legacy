from jaos_platform.base_platform_service import BasePlatformService
from logs.logger import logger


class DevelopmentWorkspaceManager(BasePlatformService):
    """Runtime-managed development workspace service."""

    SERVICE_NAME = "development_workspace_manager"

    def __init__(self, runtime=None):
        self.workspaces = {}

        super().__init__(runtime)

    def register_workspace(
        self,
        name,
        repository,
        vscode_workspace,
    ):
        self.workspaces[name] = {
            "repository": repository,
            "vscode_workspace": vscode_workspace,
        }

        logger.info(
            f"Development workspace registered: {name}"
        )

        if self.runtime is not None:
            self.runtime.events.publish(
                "development_workspace_registered",
                {
                    "name": name,
                    "repository": repository,
                    "vscode_workspace": vscode_workspace,
                },
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