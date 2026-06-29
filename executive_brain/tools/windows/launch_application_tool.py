"""
JAOS Launch Application Tool

Phase 4 — JAOS-M-0031

Launches a Windows application or executable command.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class LaunchApplicationTool(ToolInterface):
    """
    Tool for launching Windows applications.
    """

    @property
    def tool_name(self) -> str:
        return "launch_application"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        application = request.parameters.get("application")

        if not isinstance(application, str) or not application.strip():
            raise ValueError("application parameter is required")

        working_directory = request.parameters.get("working_directory")

        if working_directory is not None:
            if not isinstance(working_directory, str) or not working_directory.strip():
                raise ValueError("working_directory must be a non-empty string")

            cwd = Path(working_directory)

            if not cwd.exists() or not cwd.is_dir():
                return ToolResponse(
                    status=ToolStatus.FAILURE,
                    message="Working directory does not exist",
                    data={"working_directory": str(cwd)},
                )
        else:
            cwd = None

        try:
            process = subprocess.Popen(
                application,
                cwd=str(cwd) if cwd is not None else None,
                shell=True,
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Application launch failed",
                data={"error": str(error)},
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Application launched successfully",
            data={
                "application": application,
                "pid": process.pid,
            },
        )