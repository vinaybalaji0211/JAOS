"""
JAOS Tool Models

Phase 4 — JAOS-M-0029

Shared models for the Tool Layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ToolStatus(str, Enum):
    """
    Tool execution status.
    """

    SUCCESS = "success"
    FAILURE = "failure"


@dataclass(slots=True)
class ToolRequest:
    """
    Request passed to a tool.
    """

    tool_name: str
    parameters: dict = field(default_factory=dict)


@dataclass(slots=True)
class ToolResponse:
    """
    Response returned by a tool.
    """

    status: ToolStatus
    message: str
    data: dict = field(default_factory=dict)