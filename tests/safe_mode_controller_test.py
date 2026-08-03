from brain.safe_mode_controller import SafeModeController

controller = (
    SafeModeController()
)

controller.show_status()

controller.activate(
    "Memory Tampering Detected"
)

controller.show_status()

controller.deactivate()

controller.show_status()