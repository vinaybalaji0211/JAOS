from pathlib import Path
from shutil import copy2

from jaos.tools import (
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class CopyFileTool(ToolInterface):
    """
    Copies a file from source path to destination path.
    """

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="copy_file",
            version="1.0.0",
            description="Copies a file from source path to destination path.",
            permissions=("filesystem.copy",),
            capabilities=(ToolCapability.FILESYSTEM_COPY,),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        source_value = request.payload.get("source")
        destination_value = request.payload.get("destination")

        if not isinstance(source_value, str) or not source_value.strip():
            return ToolResult(
                success=False,
                error="Source path is required.",
            )

        if not isinstance(destination_value, str) or not destination_value.strip():
            return ToolResult(
                success=False,
                error="Destination path is required.",
            )

        source = Path(source_value)
        destination = Path(destination_value)

        if not source.exists():
            return ToolResult(
                success=False,
                error=f"Source file does not exist: {source}",
            )

        if not source.is_file():
            return ToolResult(
                success=False,
                error=f"Source path is not a file: {source}",
            )

        if destination.exists() and destination.is_dir():
            return ToolResult(
                success=False,
                error=f"Destination path is a directory: {destination}",
            )

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(source, destination)
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
            )

        return ToolResult(
            success=True,
            output={
                "source": str(source),
                "destination": str(destination),
            },
        )