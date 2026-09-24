"""
JAOS Tool Interface

Phase 4 — JAOS-M-0029

Defines the base interface that all JAOS tools must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
)


class ToolInterface(ABC):
    """
    Base interface for all executable JAOS tools.
    """

    @property
    @abstractmethod
    def tool_name(self) -> str:
        """
        Returns the unique tool name.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self, request: ToolRequest) -> ToolResponse:
        """
        Executes the tool.
        """
        raise NotImplementedError