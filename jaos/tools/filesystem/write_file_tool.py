from pathlib import Path

from jaos.tools import (
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class WriteFileTool(ToolInterface):
    """
    Writes UTF-8 text content to a file.
    """

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="write_file",
            version="1.0.0",
            description="Writes UTF-8 text content to a file.",
            permissions=("filesystem.write",),
            capabilities=(ToolCapability.FILESYSTEM_WRITE,),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        path_value = request.payload.get("path")
        content = request.payload.get("content")

        if not isinstance(path_value, str) or not path_value.strip():
            return ToolResult(
                success=False,
                error="File path is required.",
            )

        if not isinstance(content, str):
            return ToolResult(
                success=False,
                error="Content must be a string.",
            )

        path = Path(path_value)

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "bytes_written": len(content.encode("utf-8")),
            },
        )