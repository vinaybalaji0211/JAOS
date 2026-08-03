from communication.communication_hub import CommunicationHub

hub = CommunicationHub()

hub.add_event(
    "Gmail",
    "Email",
    "Interview invitation received."
)

hub.add_event(
    "GitHub",
    "Repository",
    "New pull request."
)

hub.add_event(
    "Calendar",
    "Reminder",
    "JAOS Development at 7 PM."
)

hub.show_events()