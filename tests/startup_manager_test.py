from system_services.startup_manager import (
    StartupManager
)

manager = StartupManager()

manager.register_service(
    "JAOS Core"
)

manager.register_service(
    "Notification Center"
)

manager.show_services()