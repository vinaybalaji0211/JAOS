from development.vscode_manager import VSCodeManager

manager = VSCodeManager()

manager.register_workspace(
    "JAOS Workspace",
    "JAOS"
)

manager.register_workspace(
    "YOLO Workspace",
    "YOLO Project"
)

manager.show_workspaces()