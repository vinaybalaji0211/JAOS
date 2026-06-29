"""
JAOS Close Application Tool

Phase 4 — JAOS-M-0031

Closes a running application by process ID.
"""

from __future__ import annotations

import os

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class CloseApplicationTool(ToolInterface):
    """
    Tool for terminating a running process.
    """

    @property
    def tool_name(self) -> str:
        return "close_application"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        pid = request.parameters.get("pid")

        if not isinstance(pid, int):
            raise ValueError("pid parameter must be an integer")

        try:
            os.kill(pid, 9)
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to close application",
                data={
                    "pid": pid,
                    "error": str(error),
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Application closed successfully",
            data={
                "pid": pid,
            },
        )