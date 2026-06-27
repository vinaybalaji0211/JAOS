from brain.emergency_override_handler import (
    EmergencyOverrideHandler
)

handler = EmergencyOverrideHandler()

handler.show_status()

handler.trigger(
    "UNAUTHORIZED_ACCESS"
)

handler.show_status()

handler.clear()

handler.show_status()