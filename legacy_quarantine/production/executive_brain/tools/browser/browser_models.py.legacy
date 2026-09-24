"""
JAOS Browser Models

Phase 4 — JAOS-M-0032

Shared models for browser tools and browser providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class BrowserStatus(str, Enum):
    """
    Browser operation status.
    """

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


@dataclass(slots=True)
class BrowserRequest:
    """
    Request passed to a browser provider.
    """

    action: str
    parameters: dict = field(default_factory=dict)


@dataclass(slots=True)
class BrowserResponse:
    """
    Response returned by a browser provider.
    """

    success: bool
    message: str
    data: dict = field(default_factory=dict)