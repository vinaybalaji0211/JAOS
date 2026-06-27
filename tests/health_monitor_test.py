from brain.health_monitor import (
    HealthMonitor
)

monitor = HealthMonitor()

monitor.show_health()

monitor.update(
    "providers",
    "WARNING"
)

monitor.show_health()

monitor.update(
    "voice_system",
    "FAILED"
)

monitor.show_health()