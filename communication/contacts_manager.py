from logs.logger import logger


class ContactsManager:

    def __init__(self):

        self.contacts = {}

    def add_contact(
            self,
            name,
            email,
            role):

        self.contacts[name] = {
            "email": email,
            "role": role
        }

        logger.info(
            f"Contact added: {name}"
        )

    def show_contacts(self):

        print("\n=== Contacts Manager ===\n")

        if not self.contacts:

            print("No contacts.")
            return

        for name, data in self.contacts.items():

            print(name)

            print(
                f"  Email : {data['email']}"
            )

            print(
                f"  Role  : {data['role']}"
            )

            print()