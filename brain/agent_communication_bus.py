from logs.logger import logger


class AgentCommunicationBus:

    def __init__(self):

        self.messages = []

    def send_message(
            self,
            sender,
            receiver,
            message):

        record = {
            "sender": sender,
            "receiver": receiver,
            "message": message
        }

        self.messages.append(
            record
        )

        logger.info(
            f"Message sent: "
            f"{sender} -> {receiver}"
        )

    def get_messages_for(
            self,
            receiver):

        return [
            msg
            for msg in self.messages
            if msg["receiver"] == receiver
        ]

    def show_messages(self):

        print(
            "\nAgent Communication Bus:\n"
        )

        if not self.messages:

            print(
                "No messages."
            )

            return

        for msg in self.messages:

            print(
                f"{msg['sender']} -> "
                f"{msg['receiver']}"
            )

            print(
                f"Message: "
                f"{msg['message']}"
            )

            print()