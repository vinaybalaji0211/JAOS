"""
JAOS Cookies Tool

Phase 4 — JAOS-M-0032

Detects browser cookie database locations.
"""

from __future__ import annotations

from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class CookiesTool(ToolInterface):
    """
    Tool for locating browser cookie databases.
    """

    COOKIE_PATHS = {
        "chrome": Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
        "edge": Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default/Network/Cookies",
        "brave": Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Network/Cookies",
    }

    @property
    def tool_name(self) -> str:
        return "cookies"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        browsers = []

        for browser, path in self.COOKIE_PATHS.items():
            browsers.append(
                {
                    "browser": browser,
                    "available": path.exists(),
                    "path": str(path),
                }
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Cookie locations inspected successfully",
            data={
                "browsers": browsers,
            },
        )