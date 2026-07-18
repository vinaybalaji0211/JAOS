from pathlib import Path

from jaos.tools import (
    ToolApprovalLevel,
    ToolApprovalPolicy,
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class DeleteFileTool(ToolInterface):
    """
    Deletes a file.

    Approval is enforced by ToolExecutionEngine through metadata approval policy.
    """

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="delete_file",
            version="1.0.0",
            description="Deletes a file after approval.",
            permissions=("filesystem.delete",),
            capabilities=(ToolCapability.FILESYSTEM_DELETE,),
            approval_policy=ToolApprovalPolicy(
                level=ToolApprovalLevel.DANGEROUS,
                reason="Deleting files permanently removes data.",
            ),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        path_value = request.payload.get("path")

        if not isinstance(path_value, str) or not path_value.strip():
            return ToolResult(success=False, error="File path is required.")

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
            path.unlink()
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))

        return ToolResult(
            success=True,
            output={
                "path": str(path),
                "deleted": True,
            },
        )