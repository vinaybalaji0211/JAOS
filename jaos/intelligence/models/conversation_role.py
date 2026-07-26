"""Conversation roles for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class ConversationRole(str, Enum):
    """Identifies the source role of a structured conversation turn."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    MEMORY = "memory"
    TOOL_RESULT = "tool_result"