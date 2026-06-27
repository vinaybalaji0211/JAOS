from logs.logger import logger


class IntrusionAlertSystem:

    THREAT_LEVELS = {
        "failed_login": "WARNING",
        "unauthorized_access": "ALARM",
        "secret_access_attempt": "LOCKDOWN",
        "dangerous_command": "LOCKDOWN",
        "plugin_abuse": "ALARM",
        "config_tampering": "LOCKDOWN",
        "multiple_failures": "ALARM"
    }

    @staticmethod
    def detect(event_type):

        level = IntrusionAlertSystem.THREAT_LEVELS.get(
            event_type,
            "NORMAL"
        )

        if level == "WARNING":
            action = "Warn author."

        elif level == "ALARM":
            action = "Warn author, trigger alarm, increase monitoring."

        elif level == "LOCKDOWN":
            action = (
                "Warn author, trigger alarm, lock protected systems, "
                "disable risky actions, enter safety mode."
            )

        else:
            action = "No threat detected."

        logger.warning(
            f"Security event: {event_type} | Level: {level}"
        )

        return {
            "event": event_type,
            "level": level,
            "action": action
        }

    @staticmethod
    def show_alert(event_type):

        result = IntrusionAlertSystem.detect(event_type)

        print("\nIntrusion Alert System:\n")
        print(f"Event: {result['event']}")
        print(f"Threat Level: {result['level']}")
        print(f"Action: {result['action']}")