from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import RenameFileTool


def test_rename_file_tool_metadata():
    tool = RenameFileTool()
    metadata = tool.metadata()

    assert metadata.name == "rename_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.rename",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_RENAME,
    )


def test_rename_file_tool_requires_source():
    tool = RenameFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "new_name": "target.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_rename_file_tool_requires_new_name(tmp_path):
    tool = RenameFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
            },
        )
    )

    assert result.success is False
    assert result.error == "New file name is required."


def test_rename_file_tool_rejects_path_as_new_name(tmp_path):
    tool = RenameFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "nested/target.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "New file name must not include a path."


def test_rename_file_tool_rejects_missing_source(tmp_path):
    tool = RenameFileTool()
    source = tmp_path / "missing.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "target.txt",
            },
        )
    )

    assert result.success is False
    assert "Source file does not exist" in result.error


def test_rename_file_tool_rejects_directory_source(tmp_path):
    tool = RenameFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(tmp_path),
                "new_name": "target.txt",
            },
        )
    )

    assert result.success is False
    assert "Source path is not a file" in result.error


def test_rename_file_tool_rejects_existing_destination(tmp_path):
    tool = RenameFileTool()
    source = tmp_path / "source.txt"
    destination = tmp_path / "target.txt"

    source.write_text("JAOS", encoding="utf-8")
    destination.write_text("Existing", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": destination.name,
            },
        )
    )

    assert result.success is False
    assert "Destination already exists" in result.error


def test_rename_file_tool_renames_file(tmp_path):
    tool = RenameFileTool()
    source = tmp_path / "source.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "renamed.txt",
            },
        )
    )

    destination = tmp_path / "renamed.txt"

    assert result.success is True
    assert source.exists() is False
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"


def test_rename_file_tool_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.rename",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(RenameFileTool())

    source = tmp_path / "source.txt"
    source.write_text("Manager Rename", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "manager.txt",
            },
        )
    )

    destination = tmp_path / "manager.txt"

    assert result.success is True
    assert source.exists() is False
    assert destination.read_text(encoding="utf-8") == "Manager Rename"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "rename_file"
    assert records[0].success is True