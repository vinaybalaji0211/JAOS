from pc_control.application_manager import (
    ApplicationManager
)

manager = ApplicationManager()

manager.register_application(
    "VS Code",
    "Code.exe"
)

manager.register_application(
    "Chrome",
    "chrome.exe"
)

manager.register_application(
    "Terminal",
    "cmd.exe"
)

manager.show_applications()