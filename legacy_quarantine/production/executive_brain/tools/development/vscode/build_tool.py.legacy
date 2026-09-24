"""
JAOS Build Tool

Phase 4 — JAOS-M-0033

Executes a build command inside a project directory.
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


class BuildTool(ToolInterface):
    """
    Executes a build command.
    """

    @property
    def tool_name(self) -> str:
        return "build"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        project = request.parameters.get("project")
        command = request.parameters.get("command")

        if not isinstance(project, str) or not project.strip():
            raise ValueError("project parameter is required")

        if not isinstance(command, list) or not command:
            raise ValueError("command parameter must be a non-empty list")

        project_path = Path(project)

        if not project_path.exists() or not project_path.is_dir():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Project path does not exist",
                data={"project": str(project_path)},
            )

        try:
            completed = subprocess.run(
                command,
                cwd=str(project_path),
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Build execution failed",
                data={"error": str(error)},
            )

        if completed.returncode != 0:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Build failed",
                data={
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Build completed successfully",
            data={
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            },
        )