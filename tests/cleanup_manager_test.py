from system_services.cleanup_manager import CleanupManager

cleanup = CleanupManager()

cleanup.register_cleanup(
    "Temporary Cache"
)

cleanup.register_cleanup(
    "Temporary Logs"
)

cleanup.register_cleanup(
    "Unused Generated Files"
)

cleanup.show_tasks()

cleanup.run_cleanup()