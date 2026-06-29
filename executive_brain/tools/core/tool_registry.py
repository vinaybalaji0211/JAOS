"""
JAOS Tool Registry

Phase 4 — JAOS-M-0029

Stores and manages registered JAOS tools.
"""

from __future__ import annotations

from executive_brain.tools.core.tool_interface import ToolInterface


class ToolRegistry:
    """
    Registry for all available JAOS tools.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolInterface] = {}

    def register(self, tool: ToolInterface) -> None:
        """
        Register a tool.
        """
        if not isinstance(tool, ToolInterface):
            raise TypeError("tool must implement ToolInterface")

        if tool.tool_name in self._tools:
            raise ValueError(
                f"Tool '{tool.tool_name}' is already registered."
            )

        self._tools[tool.tool_name] = tool

    def unregister(self, tool_name: str) -> None:
        """
        Remove a registered tool.
        """
        if tool_name not in self._tools:
            raise KeyError(
                f"Unknown tool '{tool_name}'."
            )

        del self._tools[tool_name]

    def get(self, tool_name: str) -> ToolInterface:
        """
        Get a registered tool.
        """
        if tool_name not in self._tools:
            raise KeyError(
                f"Unknown tool '{tool_name}'."
            )

        return self._tools[tool_name]

    def has(self, tool_name: str) -> bool:
        """
        Check whether a tool exists.
        """
        return tool_name in self._tools

    def list_tools(self) -> list[str]:
        """
        Return registered tool names.
        """
        return sorted(self._tools.keys())

    def count(self) -> int:
        """
        Number of registered tools.
        """
        return len(self._tools)

    def clear(self) -> None:
        """
        Remove all registered tools.
        """
        self._tools.clear()