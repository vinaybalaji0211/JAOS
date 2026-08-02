"""Enumeration of intelligence context categories."""

from enum import Enum


class ContextType(str, Enum):
    """Defines the type of contextual information."""

    CONVERSATION = "conversation"
    MEMORY = "memory"
    RUNTIME = "runtime"
    EXECUTIVE = "executive"
    AI = "ai"
    USER = "user"
    ENVIRONMENT = "environment"
    SYSTEM = "system"
    TASK = "task"
    SECURITY = "security"
    EXTERNAL = "external"