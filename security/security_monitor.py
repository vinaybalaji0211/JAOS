from logs.logger import logger


class SecurityMonitor:

    def __init__(self):

        self.events = []

    def record_event(
            self,
            level,
            description):

        self.events.append({
            "level": level,
            "description": description
        })

        logger.info(
            f"Security event: {level}"
        )

    def show_events(self):

        print("\n=== Security Monitor ===\n")

        if not self.events:

            print("No security events.")
            return

        for event in self.events:

            print(f"[{event['level']}] {event['description']}")