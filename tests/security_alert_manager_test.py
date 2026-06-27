from brain.security_alert_manager import (
    SecurityAlertManager
)

manager = SecurityAlertManager()

manager.create_alert(
    "Unauthorized Upgrade Attempt",
    "HIGH"
)

manager.create_alert(
    "Memory Tampering",
    "CRITICAL"
)

manager.acknowledge_alert(
    "Unauthorized Upgrade Attempt"
)

manager.show_alerts()