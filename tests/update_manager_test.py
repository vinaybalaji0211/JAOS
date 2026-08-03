from system_services.update_manager import UpdateManager

manager = UpdateManager()

manager.register_update(
    "JAOS Core Patch",
    "1.0.1-alpha"
)

manager.register_update(
    "Security Rules Update",
    "1.0.2-alpha",
    "PENDING"
)

manager.show_updates()