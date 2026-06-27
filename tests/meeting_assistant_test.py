from communication.meeting_assistant import (
    MeetingAssistant
)

assistant = MeetingAssistant()

assistant.register_meeting(
    "JAOS Architecture Review",
    "Tomorrow 10:00 AM",
    [
        "Vinay",
        "Professor"
    ]
)

assistant.register_meeting(
    "Project Planning",
    "Friday 4:00 PM",
    [
        "Vinay",
        "Rahul"
    ]
)

assistant.show_meetings()