import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.rename_file_tool import RenameFileTool


def test_rename_file_tool_name():
    tool = RenameFileTool()

    assert tool.tool_name == "rename_file"


def test_rename_file_success(tmp_path):
    source = tmp_path / "old_name.txt"
    destination = tmp_path / "new_name.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    tool = RenameFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File renamed successfully"

    assert not source.exists()
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"

    assert response.data["source"] == str(source)
    assert response.data["destination"] == str(destination)


def test_rename_missing_source(tmp_path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "new.txt"

    tool = RenameFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Source file does not exist"


def test_rename_creates_destination_directory(tmp_path):
    source = tmp_path / "file.txt"
    destination = tmp_path / "folder" / "renamed.txt"

    source.write_text("Created", encoding="utf-8")

    tool = RenameFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="rename_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Created"


def test_rename_requires_tool_request():
    tool = RenameFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_rename_requires_source():
    tool = RenameFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="rename_file",
                parameters={
                    "destination": "new.txt",
                },
            )
        )


def test_rename_requires_destination():
    tool = RenameFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="rename_file",
                parameters={
                    "source": "old.txt",
                },
            )
        )


def test_rename_rejects_empty_parameters():
    tool = RenameFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="rename_file",
                parameters={
                    "source": "   ",
                    "destination": "new.txt",
                },
            )
        )

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="rename_file",
                parameters={
                    "source": "old.txt",
                    "destination": "   ",
                },
            )
        )