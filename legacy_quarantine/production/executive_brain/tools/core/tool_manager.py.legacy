"""
JAOS Tool Manager

Phase 4 — JAOS-M-0029

Executes tools through the Tool Registry.
"""

from __future__ import annotations

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
)
from executive_brain.tools.core.tool_registry import ToolRegistry


class ToolManager:
    """
    Central manager for executing JAOS tools.
    """

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self._registry = registry or ToolRegistry()

    @property
    def registry(self) -> ToolRegistry:
        """
        Returns the underlying tool registry.
        """
        return self._registry

    def register_tool(self, tool: ToolInterface) -> None:
        """
        Register a tool.
        """
        self._registry.register(tool)

    def unregister_tool(self, tool_name: str) -> None:
        """
        Remove a tool from the registry.
        """
        self._registry.unregister(tool_name)

    def has_tool(self, tool_name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return self._registry.has(tool_name)

    def list_tools(self) -> list[str]:
        """
        List registered tools.
        """
        return self._registry.list_tools()

    def execute(self, request: ToolRequest) -> ToolResponse:
        """
        Execute a registered tool.
        """
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        if not request.tool_name.strip():
            raise ValueError("tool_name cannot be empty")

        tool = self._registry.get(request.tool_name)
        return tool.execute(request)
