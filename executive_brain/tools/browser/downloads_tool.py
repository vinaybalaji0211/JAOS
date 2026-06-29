"""
JAOS Downloads Tool

Phase 4 — JAOS-M-0032

Opens the browser downloads page.
"""

from __future__ import annotations

import webbrowser

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class DownloadsTool(ToolInterface):
    """
    Tool for opening the browser downloads page.
    """

    @property
    def tool_name(self) -> str:
        return "downloads"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        provider = request.parameters.get("provider", "chrome")

        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("provider must be a non-empty string")

        provider = provider.lower().strip()

        urls = {
            "chrome": "chrome://downloads/",
            "edge": "edge://downloads/",
            "brave": "brave://downloads/",
        }

        if provider not in urls:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Unsupported browser provider",
                data={
                    "provider": provider,
                    "supported_providers": sorted(urls.keys()),
                },
            )

        success = webbrowser.open(urls[provider])

        if not success:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to open downloads page",
                data={
                    "provider": provider,
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Downloads page opened successfully",
            data={
                "provider": provider,
                "url": urls[provider],
            },
        )