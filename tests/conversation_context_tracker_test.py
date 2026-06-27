from brain.conversation_context_tracker import (
    ConversationContextTracker
)

tracker = ConversationContextTracker()

tracker.change_topic(
    "Executive Brain"
)

tracker.change_topic(
    "Voice System"
)

tracker.show_context()