"""
JAOS AI Provider Models

Phase 3 — JAOS-M-0023
Shared data models for communication between the Executive Brain
and AI providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AIProviderStatus(str, Enum):
    """
    Current status of an AI provider.
    """

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


@dataclass(slots=True)
class AIProviderRequest:
    """
    Standard request object sent to any AI provider.
    """

    prompt: str
    system_prompt: str = ""
    conversation: list[dict[str, str]] = field(default_factory=list)
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AIProviderResponse:
    """
    Standard response object returned by any AI provider.
    """

    success: bool
    content: str
    provider: str
    model: str
    metadata: dict[str, Any] = field(default_factory=dict)