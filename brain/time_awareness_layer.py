from datetime import datetime

from logs.logger import logger


class TimeAwarenessLayer:

    @staticmethod
    def get_time_info():

        now = datetime.now()

        hour = now.hour

        if 5 <= hour < 12:
            period = "Morning"

        elif 12 <= hour < 17:
            period = "Afternoon"

        elif 17 <= hour < 21:
            period = "Evening"

        else:
            period = "Night"

        info = {

            "date": now.strftime("%Y-%m-%d"),

            "time": now.strftime("%H:%M:%S"),

            "period": period,

            "weekday": now.strftime("%A")

        }

        logger.info(
            "Time awareness updated."
        )

        return info

    @staticmethod
    def show_time():

        info = (
            TimeAwarenessLayer
            .get_time_info()
        )

        print("\nTime Awareness:\n")

        for key, value in info.items():

            print(
                f"{key}: {value}"
            )