from communication.calendar_manager import CalendarManager
from communication.communication_hub import CommunicationHub
from communication.contacts_manager import ContactsManager
from communication.conversation_manager import ConversationManager
from communication.email_manager import EmailManager
from communication.meeting_assistant import MeetingAssistant

print("\n===== COMMUNICATION PLATFORM TEST =====\n")

email = EmailManager()
email.register_account(
    "Gmail",
    "vinay@example.com"
)

calendar = CalendarManager()
calendar.add_event(
    "JAOS Development",
    "Today 7:00 PM"
)

contacts = ContactsManager()
contacts.add_contact(
    "Professor",
    "prof@example.com",
    "Faculty"
)

hub = CommunicationHub()
hub.add_event(
    "Gmail",
    "Email",
    "Architecture review invitation."
)

conversation = ConversationManager()
conversation.register_conversation(
    "Discord",
    "JAOS Dev",
    "Platform completed."
)

meeting = MeetingAssistant()
meeting.register_meeting(
    "Architecture Review",
    "Tomorrow 10:00 AM",
    [
        "Vinay",
        "Professor"
    ]
)

print("\n===== COMPONENT STATUS =====\n")

email.show_accounts()
calendar.show_events()
contacts.show_contacts()
hub.show_events()
conversation.show_conversations()
meeting.show_meetings()

print("\n===== COMMUNICATION PLATFORM COMPLETE =====")