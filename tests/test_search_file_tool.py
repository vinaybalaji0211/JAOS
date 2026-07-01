from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import SearchFileTool


def test_search_file_tool_metadata():
    tool = SearchFileTool()
    metadata = tool.metadata()

    assert metadata.name == "search_file"
    assert metadata.permissions == ("filesystem.search",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_SEARCH,
    )


def test_search_requires_root():
    tool = SearchFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="search_file",
            payload={},
        )
    )

    assert result.success is False
    assert result.error == "Search root is required."


def test_search_requires_existing_directory(tmp_path):
    tool = SearchFileTool()

    missing = tmp_path / "missing"

    result = tool.execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(missing),
            },
        )
    )

    assert result.success is False
    assert "does not exist" in result.error


def test_search_finds_matching_files(tmp_path):
    tool = SearchFileTool()

    (tmp_path / "a.py").write_text("print()", encoding="utf-8")
    (tmp_path / "b.py").write_text("print()", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.py",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 2


def test_search_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.search",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(SearchFileTool())

    (tmp_path / "hello.md").write_text("# JAOS", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.md",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 1

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "search_file"
    assert records[0].success is True