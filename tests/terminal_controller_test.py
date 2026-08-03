from pc_control.terminal_controller import TerminalController

terminal = TerminalController()

terminal.register_command(
    "git status"
)

terminal.register_command(
    "python train.py"
)

terminal.register_command(
    "pip install ultralytics"
)

terminal.show_commands()