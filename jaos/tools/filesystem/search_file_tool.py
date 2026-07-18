from pathlib import Path

from jaos.tools import (
    ToolCapability,
    ToolInterface,
    ToolMetadata,
    ToolRequest,
    ToolResult,
)


class SearchFileTool(ToolInterface):
    """
    Recursively searches for files using a glob pattern.
    """

    DEFAULT_PATTERN = "*"
    DEFAULT_MAX_RESULTS = 100

    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="search_file",
            version="1.0.0",
            description="Searches for files recursively.",
            permissions=("filesystem.search",),
            capabilities=(ToolCapability.FILESYSTEM_SEARCH,),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        root = request.payload.get("root")
        pattern = request.payload.get("pattern", self.DEFAULT_PATTERN)
        max_results = request.payload.get(
            "max_results",
            self.DEFAULT_MAX_RESULTS,
        )

        if not isinstance(root, str) or not root.strip():
            return ToolResult(
                success=False,
                error="Search root is required.",
            )

        if not isinstance(pattern, str) or not pattern.strip():
            return ToolResult(
                success=False,
                error="Search pattern is required.",
            )

        if not isinstance(max_results, int) or max_results <= 0:
            return ToolResult(
                success=False,
                error="max_results must be a positive integer.",
            )

        root_path = Path(root)

        if not root_path.exists():
            return ToolResult(
                success=False,
                error=f"Root directory does not exist: {root_path}",
            )

        if not root_path.is_dir():
            return ToolResult(
                success=False,
                error=f"Root path is not a directory: {root_path}",
            )

        matches = []

        for path in root_path.rglob(pattern):
            if path.is_file():
                matches.append(str(path.resolve()))

            if len(matches) >= max_results:
                break

        return ToolResult(
            success=True,
            output={
                "root": str(root_path.resolve()),
                "pattern": pattern,
                "count": len(matches),
                "matches": matches,
            },
        )