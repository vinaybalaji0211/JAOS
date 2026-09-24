"""
JAOS VS Code Project Tool

Phase 4 — JAOS-M-0033

Opens a project in Visual Studio Code.
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


class ProjectTool(ToolInterface):
    """
    Opens a project in VS Code.
    """

    @property
    def tool_name(self) -> str:
        return "project"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        project = request.parameters.get("project")

        if not isinstance(project, str) or not project.strip():
            raise ValueError("project parameter is required")

        project_path = Path(project)

        if not project_path.exists():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Project path does not exist",
                data={
                    "project": str(project_path),
                },
            )

        try:
            subprocess.Popen(
                ["code", str(project_path)],
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to open VS Code project",
                data={
                    "error": str(error),
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="VS Code project opened successfully",
            data={
                "project": str(project_path),
            },
        )