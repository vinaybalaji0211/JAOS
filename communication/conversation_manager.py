from logs.logger import logger


class ConversationManager:

    def __init__(self):

        self.conversations = {}

    def register_conversation(
            self,
            provider,
            conversation_name,
            latest_message):

        self.conversations[conversation_name] = {

            "provider": provider,

            "latest_message": latest_message

        }

        logger.info(

            f"Conversation registered: {conversation_name}"

        )

    def show_conversations(self):

        print(

            "\n=== Conversation Manager ===\n"

        )

        if not self.conversations:

            print(

                "No conversations."

            )

            return

        for name, data in self.conversations.items():

            print(name)

            print(

                f"  Provider : {data['provider']}"

            )

            print(

                f"  Latest   : {data['latest_message']}"

            )

            print()