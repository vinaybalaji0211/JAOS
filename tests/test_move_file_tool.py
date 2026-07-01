from jaos.tools import (
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import MoveFileTool


def test_move_file_tool_metadata():
    tool = MoveFileTool()
    metadata = tool.metadata()

    assert metadata.name == "move_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.move",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_MOVE,
    )


def test_move_file_tool_requires_source():
    tool = MoveFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "destination": "target.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_move_file_tool_requires_destination(tmp_path):
    tool = MoveFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(source),
            },
        )
    )

    assert result.success is False
    assert result.error == "Destination path is required."


def test_move_file_tool_rejects_missing_source(tmp_path):
    tool = MoveFileTool()
    source = tmp_path / "missing.txt"
    destination = tmp_path / "target.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert "Source file does not exist" in result.error


def test_move_file_tool_rejects_directory_source(tmp_path):
    tool = MoveFileTool()
    destination = tmp_path / "target.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(tmp_path),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert "Source path is not a file" in result.error


def test_move_file_tool_rejects_directory_destination(tmp_path):
    tool = MoveFileTool()
    source = tmp_path / "source.txt"
    source.write_text("JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(source),
                "destination": str(tmp_path),
            },
        )
    )

    assert result.success is False
    assert "Destination path is a directory" in result.error


def test_move_file_tool_moves_file(tmp_path):
    tool = MoveFileTool()
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "target.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert source.exists() is False
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"


def test_move_file_tool_integrates_with_manager(tmp_path):
    permissions = ToolPermissionManager(("filesystem.move",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(MoveFileTool())

    source = tmp_path / "source.txt"
    destination = tmp_path / "target.txt"

    source.write_text("Manager Move", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="move_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert source.exists() is False
    assert destination.read_text(encoding="utf-8") == "Manager Move"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "move_file"
    assert records[0].success is True