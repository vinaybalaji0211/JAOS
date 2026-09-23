"""
JAOS Prompt Models

Phase 3 — JAOS-M-0025

Provider-independent prompt models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PromptRole(str, Enum):
    """
    Supported prompt message roles.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(slots=True)
class PromptMessage:
    """
    Represents a single prompt message.
    """

    role: PromptRole
    content: str


@dataclass(slots=True)
class PromptRequest:
    """
    Represents a prompt request passed to the Prompt Engine.
    """

    messages: list[PromptMessage] = field(default_factory=list)


@dataclass(slots=True)
class PromptResponse:
    """
    Represents a validated prompt ready for an AI provider.
    """

    prompt: str
    message_count: init