"""
JAOS Browser Automation Tool

Phase 4 — JAOS-M-0032

Opens a URL using the system's default browser.
"""

from __future__ import annotations

import webbrowser

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class BrowserAutomationTool(ToolInterface):
    """
    Tool for opening URLs.
    """

    @property
    def tool_name(self) -> str:
        return "browser_automation"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        url = request.parameters.get("url")

        if not isinstance(url, str) or not url.strip():
            raise ValueError("url parameter is required")

        success = webbrowser.open(url)

        if not success:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to open browser",
                data={
                    "url": url,
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Browser opened successfully",
            data={
                "url": url,
            },
        )