from pathlib import Path

from jaos.tools import (
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class ReadFileTool(ToolInterface):
    """
    Reads text content from a file.
    """

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="read_file",
            version="1.0.0",
            description="Reads text content from a file.",
            permissions=("filesystem.read",),
            capabilities=(ToolCapability.FILESYSTEM_READ,),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        path_value = request.payload.get("path")

        if not isinstance(path_value, str) or not path_value.strip():
            return ToolResult(
                success=False,
                error="File path is required.",
            )

        path = Path(path_value)

        if not path.exists():
            return ToolResult(
                success=False,
                error=f"File does not exist: {path}",
            )

        if not path.is_file():
            return ToolResult(
                success=False,
                error=f"Path is not a file: {path}",
            )

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return ToolResult(
                success=False,
                error=f"File is not valid UTF-8 text: {path}",
            )

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "content": content,
            },
        )