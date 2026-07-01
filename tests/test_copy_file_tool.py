from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import CopyFileTool


def test_copy_file_tool_metadata():
    tool = CopyFileTool()
    metadata = tool.metadata()

    assert metadata.name == "copy_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.copy",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_COPY,
    )


def test_copy_file_tool_requires_source():
    tool = CopyFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "destination": "target.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_copy_file_tool_requires_destination(tmp_path):
    tool = CopyFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
            },
        )
    )

    assert result.success is False
    assert result.error == "Destination path is required."


def test_copy_file_tool_rejects_missing_source(tmp_path):
    tool = CopyFileTool()
    source = tmp_path / "missing.txt"
    destination = tmp_path / "target.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert "Source file does not exist" in result.error


def test_copy_file_tool_rejects_directory_source(tmp_path):
    tool = CopyFileTool()
    destination = tmp_path / "target.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(tmp_path),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert "Source path is not a file" in result.error


def test_copy_file_tool_rejects_directory_destination(tmp_path):
    tool = CopyFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(tmp_path),
            },
        )
    )

    assert result.success is False
    assert "Destination path is a directory" in result.error


def test_copy_file_tool_copies_file(tmp_path):
    tool = CopyFileTool()
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "target.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"
    assert source.read_text(encoding="utf-8") == "Hello JAOS"


def test_copy_file_tool_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.copy",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(CopyFileTool())

    source = tmp_path / "source.txt"
    destination = tmp_path / "target.txt"

    source.write_text("Manager Copy", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert destination.read_text(encoding="utf-8") == "Manager Copy"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "copy_file"
    assert records[0].success is True