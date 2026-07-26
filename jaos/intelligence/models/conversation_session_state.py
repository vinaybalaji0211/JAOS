"""Conversation session states for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class ConversationSessionState(str, Enum):
    """Describes the lifecycle state of a conversation session."""

    ACTIVE = "active"
    INTERRUPTED = "interrupted"
    CLOSED = "closed"
    FAILED = "failed"