from development.development_workspace_manager import DevelopmentWorkspaceManager

manager = DevelopmentWorkspaceManager()

manager.register_workspace(
    "JAOS Development",
    "JAOS",
    "JAOS Workspace"
)

manager.register_workspace(
    "YOLO Development",
    "YOLO Project",
    "YOLO Workspace"
)

manager.show_workspaces()