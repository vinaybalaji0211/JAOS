"""
JAOS Read File Tool

Phase 4 — JAOS-M-0030

Reads text content from a file.
"""

from __future__ import annotations

from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class ReadFileTool(ToolInterface):
    """
    Tool for reading text files.
    """

    @property
    def tool_name(self) -> str:
        return "read_file"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        path_value = request.parameters.get("path")

        if not isinstance(path_value, str) or not path_value.strip():
            raise ValueError("path parameter is required")

        file_path = Path(path_value)

        if not file_path.exists():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="File does not exist",
                data={"path": str(file_path)},
            )

        if not file_path.is_file():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Path is not a file",
                data={"path": str(file_path)},
            )

        content = file_path.read_text(encoding="utf-8")

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="File read successfully",
            data={
                "path": str(file_path),
                "content": content,
            },
        )