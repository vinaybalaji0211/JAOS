"""
JAOS Process Manager Tool

Phase 4 — JAOS-M-0031

Lists running system processes.
"""

from __future__ import annotations

import subprocess

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class ProcessManagerTool(ToolInterface):
    """
    Tool for listing running Windows processes.
    """

    @property
    def tool_name(self) -> str:
        return "process_manager"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        try:
            completed = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError as error:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Failed to list processes",
                data={"error": str(error)},
            )

        if completed.returncode != 0:
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Process listing failed",
                data={
                    "returncode": completed.returncode,
                    "stderr": completed.stderr,
                },
            )

        processes = self._parse_tasklist_output(completed.stdout)

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="Processes listed successfully",
            data={
                "count": len(processes),
                "processes": processes,
            },
        )

    def _parse_tasklist_output(self, output: str) -> list[dict[str, str]]:
        lines = output.splitlines()

        process_lines = [
            line
            for line in lines
            if line.strip()
            and not line.startswith("=")
            and not line.lower().startswith("image name")
        ]

        processes: list[dict[str, str]] = []

        for line in process_lines:
            parts = line.split()

            if len(parts) < 2:
                continue

            processes.append(
                {
                    "image_name": parts[0],
                    "pid": parts[1],
                    "raw": line,
                }
            )

        return processes