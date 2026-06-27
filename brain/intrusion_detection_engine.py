from logs.logger import logger


class IntrusionDetectionEngine:

    def __init__(self):

        self.detected_events = []

    def detect(
            self,
            event,
            risk_level):

        detection = {
            "event": event,
            "risk": risk_level,
            "status": "DETECTED"
        }

        self.detected_events.append(
            detection
        )

        logger.warning(
            f"Intrusion detected: {event}"
        )

    def show_detections(self):

        print(
            "\nIntrusion Detection Engine:\n"
        )

        if not self.detected_events:

            print(
                "No detections."
            )

            return

        for item in self.detected_events:

            print(
                f"Event: "
                f"{item['event']}"
            )

            print(
                f"Risk: "
                f"{item['risk']}"
            )

            print(
                f"Status: "
                f"{item['status']}"
            )

            print()