from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import WriteFileTool


def test_write_file_tool_metadata():
    tool = WriteFileTool()
    metadata = tool.metadata()

    assert metadata.name == "write_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.write",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_WRITE,
    )


def test_write_file_tool_requires_path():
    tool = WriteFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="write_file",
            payload={"content": "hello"},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_write_file_tool_requires_string_content():
    tool = WriteFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": "example.txt",
                "content": 123,
            },
        )
    )

    assert result.success is False
    assert result.error == "Content must be a string."


def test_write_file_tool_writes_file(tmp_path):
    tool = WriteFileTool()

    file_path = tmp_path / "output.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Hello JAOS",
            },
        )
    )

    assert result.success is True
    assert file_path.read_text(encoding="utf-8") == "Hello JAOS"


def test_write_file_tool_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.write",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(WriteFileTool())

    file_path = tmp_path / "manager.txt"

    result = manager.execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Manager Write",
            },
        )
    )

    assert result.success is True
    assert file_path.read_text(encoding="utf-8") == "Manager Write"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "write_file"
    assert records[0].success is True