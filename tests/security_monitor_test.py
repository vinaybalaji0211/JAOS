from security.security_monitor import SecurityMonitor

monitor = SecurityMonitor()

monitor.record_event(
    "LOW",
    "VS Code opened."
)

monitor.record_event(
    "HIGH",
    "Permission denied for deleting system files."
)

monitor.show_events()