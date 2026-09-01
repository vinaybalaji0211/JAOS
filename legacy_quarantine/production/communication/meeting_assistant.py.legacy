from logs.logger import logger


class MeetingAssistant:

    def __init__(self):

        self.meetings = {}

    def register_meeting(
            self,
            title,
            schedule,
            participants):

        self.meetings[title] = {
            "schedule": schedule,
            "participants": participants
        }

        logger.info(
            f"Meeting registered: {title}"
        )

    def show_meetings(self):

        print("\n=== Meeting Assistant ===\n")

        if not self.meetings:

            print("No meetings.")
            return

        for title, data in self.meetings.items():

            print(title)
            print(f"  Schedule    : {data['schedule']}")
            print(f"  Participants: {', '.join(data['participants'])}")
            print()