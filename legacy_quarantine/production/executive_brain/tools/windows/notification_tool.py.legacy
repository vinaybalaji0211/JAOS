"""
JAOS Notification Tool

Phase 4 — JAOS-M-0031

Displays a simple Windows notification dialog.
"""

from __future__ import annotations

import ctypes

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class NotificationTool(ToolInterface):
    """
    Tool for displaying notifications.
    """

    @property
    def tool_name(self) -> str:
        return "notification"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        title = request.parameters.get("title", "JAOS")
        message = request.parameters.get("message")

        if not isinstance(message, str) or not message.strip():
            raise ValueError("message parameter is required")

        if not isinstance(title, str):
            raise ValueError("title must be a string")

        try:
            ctypes.windll.user32.MessageBoxW(
                0,
                message,
                title,
                0,
            )
        except Exception as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Notification failed",
                data={
                    "error": str(error),
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Notification displayed successfully",
            data={
                "title": title,
                "message": message,
            },
        )