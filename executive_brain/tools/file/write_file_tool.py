"""
JAOS Write File Tool

Phase 4 — JAOS-M-0030

Writes text content to a file.
"""

from __future__ import annotations

from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class WriteFileTool(ToolInterface):
    """
    Tool for writing text files.
    """

    @property
    def tool_name(self) -> str:
        return "write_file"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        path_value = request.parameters.get("path")
        content = request.parameters.get("content")

        if not isinstance(path_value, str) or not path_value.strip():
            raise ValueError("path parameter is required")

        if not isinstance(content, str):
            raise ValueError("content parameter must be a string")

        file_path = Path(path_value)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message="File written successfully",
            data={
                "path": str(file_path),
                "size": len(content),
            },
        )