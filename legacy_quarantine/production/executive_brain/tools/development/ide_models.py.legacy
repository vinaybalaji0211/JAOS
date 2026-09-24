"""
JAOS IDE Models

Phase 4 — JAOS-M-0033

Shared models for development environment providers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class IDEStatus(str, Enum):
    """
    IDE availability status.
    """

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


@dataclass(slots=True)
class IDERequest:
    """
    Request passed to an IDE provider.
    """

    action: str
    parameters: dict = field(default_factory=dict)


@dataclass(slots=True)
class IDEResponse:
    """
    Response returned by an IDE provider.
    """

    success: bool
    message: str
    data: dict = field(default_factory=dict)