from communication.contacts_manager import (
    ContactsManager
)

contacts = ContactsManager()

contacts.add_contact(
    "Rahul",
    "rahul@example.com",
    "Friend"
)

contacts.add_contact(
    "Professor",
    "prof@example.com",
    "Faculty"
)

contacts.show_contacts()