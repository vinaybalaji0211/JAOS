import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.move_file_tool import MoveFileTool


def test_move_file_tool_name():
    tool = MoveFileTool()

    assert tool.tool_name == "move_file"


def test_move_file_success(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    tool = MoveFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="move_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File moved successfully"

    assert not source.exists()
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"

    assert response.data["source"] == str(source)
    assert response.data["destination"] == str(destination)


def test_move_creates_destination_directory(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "folder" / "move.txt"

    source.write_text("Created", encoding="utf-8")

    tool = MoveFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="move_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Created"


def test_move_missing_source(tmp_path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "move.txt"

    tool = MoveFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="move_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Source file does not exist"


def test_move_requires_tool_request():
    tool = MoveFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_move_requires_source():
    tool = MoveFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="move_file",
                parameters={
                    "destination": "move.txt",
                },
            )
        )


def test_move_requires_destination():
    tool = MoveFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="move_file",
                parameters={
                    "source": "source.txt",
                },
            )
        )


def test_move_rejects_empty_parameters():
    tool = MoveFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="move_file",
                parameters={
                    "source": "   ",
                    "destination": "move.txt",
                },
            )
        )

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="move_file",
                parameters={
                    "source": "source.txt",
                    "destination": "   ",
                },
            )
        )