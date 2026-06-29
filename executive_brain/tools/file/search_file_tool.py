"""
JAOS Search File Tool

Phase 4 — JAOS-M-0030

Searches for files using a recursive glob pattern.
"""

from __future__ import annotations

from pathlib import Path

from executive_brain.tools.core.tool_interface import ToolInterface
from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolResponse,
    ToolStatus,
)


class SearchFileTool(ToolInterface):
    """
    Tool for searching files recursively.
    """

    @property
    def tool_name(self) -> str:
        return "search_file"

    def execute(self, request: ToolRequest) -> ToolResponse:
        if not isinstance(request, ToolRequest):
            raise TypeError("request must be a ToolRequest")

        path_value = request.parameters.get("path")
        pattern = request.parameters.get("pattern")

        if not isinstance(path_value, str) or not path_value.strip():
            raise ValueError("path parameter is required")

        if not isinstance(pattern, str) or not pattern.strip():
            raise ValueError("pattern parameter is required")

        root = Path(path_value)

        if not root.exists():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Search path does not exist",
                data={"path": str(root)},
            )

        if not root.is_dir():
            return ToolResponse(
                status=ToolStatus.FAILURE,
                message="Search path is not a directory",
                data={"path": str(root)},
            )

        matches = [
            str(file)
            for file in root.rglob(pattern)
            if file.is_file()
        ]

        return ToolResponse(
            status=ToolStatus.SUCCESS,
            message=f"Found {len(matches)} matching file(s)",
            data={
                "path": str(root),
                "pattern": pattern,
                "matches": matches,
            },
        )