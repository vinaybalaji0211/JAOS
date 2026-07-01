from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import ReadFileTool


def test_read_file_tool_metadata():
    tool = ReadFileTool()
    metadata = tool.metadata()

    assert metadata.name == "read_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.read",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_READ,)


def test_read_file_tool_requires_path():
    tool = ReadFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="read_file",
            payload={},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_read_file_tool_missing_file(tmp_path):
    tool = ReadFileTool()
    missing_file = tmp_path / "missing.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(missing_file)},
        )
    )

    assert result.success is False
    assert "File does not exist" in result.error


def test_read_file_tool_rejects_directory(tmp_path):
    tool = ReadFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(tmp_path)},
        )
    )

    assert result.success is False
    assert "Path is not a file" in result.error


def test_read_file_tool_reads_file(tmp_path):
    tool = ReadFileTool()
    file_path = tmp_path / "hello.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.output["path"] == str(file_path)
    assert result.output["content"] == "Hello JAOS"


def test_read_file_tool_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.read",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(ReadFileTool())

    file_path = tmp_path / "hello.txt"
    file_path.write_text("Hello through manager", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.output["content"] == "Hello through manager"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "read_file"
    assert records[0].success is True