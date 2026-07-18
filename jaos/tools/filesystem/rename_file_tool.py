from pathlib import Path

from jaos.tools import (
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class RenameFileTool(ToolInterface):
    """
    Renames a file.

    Payload:
    - source: existing file path
    - new_name: new file name only, not a full path
    """

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="rename_file",
            version="1.0.0",
            description="Renames a file in its current directory.",
            permissions=("filesystem.rename",),
            capabilities=(ToolCapability.FILESYSTEM_RENAME,),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        source_value = request.payload.get("source")
        new_name_value = request.payload.get("new_name")

        if not isinstance(source_value, str) or not source_value.strip():
            return ToolResult(success=False, error="Source path is required.")

        if not isinstance(new_name_value, str) or not new_name_value.strip():
            return ToolResult(success=False, error="New file name is required.")

        source = Path(source_value)
        new_name = new_name_value.strip()

        if Path(new_name).name != new_name:
            return ToolResult(
                success=False,
                error="New file name must not include a path.",
            )

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

        destination = source.with_name(new_name)

        if destination.exists():
            return ToolResult(
                success=False,
                error=f"Destination already exists: {destination}",
            )

        try:
            source.rename(destination)
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))

        return ToolResult(
            success=True,
            output={
                "source": str(source),
                "destination": str(destination),
            },
        )