from brain.continuous_monitor import (
    ContinuousMonitor
)


monitor = ContinuousMonitor()

monitor.show_status()

monitor.update_status(
    "plugins",
    "WARNING"
)

monitor.update_status(
    "security",
    "ALERT"
)

monitor.show_status()
