from datetime import datetime

from logs.logger import logger


class SessionManager:

    def __init__(self):

        self.session = {
            "started_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "status": "ACTIVE",
            "events": []
        }

        logger.info(
            "Session started."
        )

    def add_event(self, event):

        self.session["events"].append(
            {
                "time": datetime.now().strftime(
                    "%H:%M:%S"
                ),
                "event": event
            }
        )

        logger.info(
            f"Session event added: {event}"
        )

    def get_session(self):

        return self.session

    def show_session(self):

        print("\nSession Information:")

        print(
            f"Started At: {self.session['started_at']}"
        )

        print(
            f"Status: {self.session['status']}"
        )

        print("Events:")

        if not self.session["events"]:

            print("No session events.")

        else:

            for item in self.session["events"]:

                print(
                    f"- {item['time']} : {item['event']}"
                )