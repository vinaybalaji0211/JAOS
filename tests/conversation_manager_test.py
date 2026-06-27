from communication.conversation_manager import (
    ConversationManager
)

manager = ConversationManager()

manager.register_conversation(
    "WhatsApp",
    "Family",
    "Dinner at 8 PM"
)

manager.register_conversation(
    "Discord",
    "JAOS Dev",
    "New architecture uploaded"
)

manager.show_conversations()