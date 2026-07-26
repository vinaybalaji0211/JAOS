"""Context types for the JAOS AI Intelligence Platform."""

from enum import Enum, unique


@unique
class IntelligenceContextType(str, Enum):
    """Classifies context without replacing AI Platform context models."""

    SYSTEM = "system"
    USER = "user"
    CONVERSATION = "conversation"
    MEMORY = "memory"
    IDENTITY = "identity"
    RUNTIME = "runtime"
    CAPABILITY = "capability"
    TOOL_RESULT = "tool_result"
    PERMISSION = "permission"
    PROJECT = "project"