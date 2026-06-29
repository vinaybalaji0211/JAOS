"""
JAOS Git Tool

Phase 4 — JAOS-M-0033

Executes Git commands inside a repository.
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


class GitTool(ToolInterface):
    """
    Executes Git commands.
    """

    @property
    def tool_name(self) -> str:
        return "git"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        repository = request.parameters.get("repository")
        command = request.parameters.get("command")

        if not isinstance(repository, str) or not repository.strip():
            raise ValueError("repository parameter is required")

        if not isinstance(command, list) or not command:
            raise ValueError("command parameter must be a non-empty list")

        repository_path = Path(repository)

        if not repository_path.exists() or not repository_path.is_dir():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Repository path does not exist",
                data={"repository": str(repository_path)},
            )

        try:
            completed = subprocess.run(
                ["git", *command],
                cwd=str(repository_path),
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Git execution failed",
                data={"error": str(error)},
            )

        if completed.returncode != 0:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Git command failed",
                data={
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
            )

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Git command completed successfully",
            data={
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            },
        )