from pc_control.window_manager import WindowManager

manager = WindowManager()

manager.register_window(
    "VS Code - JAOS",
    "VS Code"
)

manager.register_window(
    "Chrome - ChatGPT",
    "Chrome"
)

manager.register_window(
    "Terminal",
    "Command Prompt"
)

manager.show_windows()