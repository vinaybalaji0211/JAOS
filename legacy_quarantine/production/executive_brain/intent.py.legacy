from datetime import datetime
from uuid import uuid4


class Intent:

    def __init__(
            self,
            intent_type,
            source="USER",
            priority="NORMAL"):

        self.intent_id = str(uuid4())

        self.intent_type = intent_type

        self.source = source

        self.priority = priority

        self.status = "UNDERSTOOD"

        self.created_at = datetime.now()

        self.metadata = {}

    def add_metadata(
            self,
            key,
            value):

        self.metadata[key] = value

    def update_status(
            self,
            status):

        self.status = status

    def show(self):

        print("\n========== INTENT ==========\n")

        print(f"ID        : {self.intent_id}")

        print(f"Type      : {self.intent_type}")

        print(f"Source    : {self.source}")

        print(f"Priority  : {self.priority}")

        print(f"Status    : {self.status}")

        print(f"Created   : {self.created_at}")

        print("\nMetadata")

        if not self.metadata:

            print("None")

        else:

            for key, value in self.metadata.items():

                print(f"{key}: {value}")