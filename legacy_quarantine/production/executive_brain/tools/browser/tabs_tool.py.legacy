"""
JAOS Tabs Tool

Phase 4 — JAOS-M-0032

Opens a URL in a browser tab.
"""

from __future__ import annotations

import webbrowser

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class TabsTool(ToolInterface):
    """
    Tool for opening browser tabs.
    """

    @property
    def tool_name(self) -> str:
        return "tabs"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        url = request.parameters.get("url")

        if not isinstance(url, str) or not url.strip():
            raise ValueError("url parameter is required")

        success = webbrowser.open_new_tab(url)

        if not success:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to open browser tab",
                data={"url": url},
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Browser tab opened successfully",
            data={"url": url},
        )