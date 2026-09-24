"""
JAOS Move File Tool

Phase 4 — JAOS-M-0030

Moves a file from one location to another.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class MoveFileTool(ToolInterface):
    """
    Tool for moving files.
    """

    @property
    def tool_name(self) -> str:
        return "move_file"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        source = request.parameters.get("source")
        destination = request.parameters.get("destination")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("source parameter is required")

        if not isinstance(destination, str) or not destination.strip():
            raise ValueError("destination parameter is required")

        source_path = Path(source)
        destination_path = Path(destination)

        if not source_path.exists():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Source file does not exist",
                data={"source": str(source_path)},
            )

        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(source_path), str(destination_path))

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="File moved successfully",
            data={
                "source": str(source_path),
                "destination": str(destination_path),
            },
        )