from datetime import datetime
from logs.logger import logger


class UnsupportedRequestLogger:

    def __init__(self):

        self.requests = []

    def log_request(
            self,
            request,
            planned_version):

        record = {
            "request": request,
            "planned_version": planned_version,
            "timestamp": datetime.now()
        }

        self.requests.append(record)

        logger.info(
            f"Unsupported request logged: "
            f"{request}"
        )

    def show_requests(self):

        print(
            "\nUnsupported Requests:\n"
        )

        if not self.requests:

            print(
                "No unsupported requests."
            )

            return

        for index, item in enumerate(
                self.requests,
                start=1):

            print(f"{index}.")

            print(
                f"Request: "
                f"{item['request']}"
            )

            print(
                f"Planned Version: "
                f"{item['planned_version']}"
            )

            print(
                f"Timestamp: "
                f"{item['timestamp']}"
            )

            print()