import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.copy_file_tool import CopyFileTool


def test_copy_file_tool_name():
    tool = CopyFileTool()

    assert tool.tool_name == "copy_file"


def test_copy_file_success(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"

    source.write_text("Hello JAOS", encoding="utf-8")

    tool = CopyFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File copied successfully"

    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"

    assert response.data["source"] == str(source)
    assert response.data["destination"] == str(destination)


def test_copy_creates_destination_directory(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "folder" / "copy.txt"

    source.write_text("Created", encoding="utf-8")

    tool = CopyFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert destination.exists()
    assert destination.read_text(encoding="utf-8") == "Created"


def test_copy_missing_source(tmp_path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "copy.txt"

    tool = CopyFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="copy_file",
            parameters={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Source file does not exist"


def test_copy_requires_tool_request():
    tool = CopyFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_copy_requires_source():
    tool = CopyFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="copy_file",
                parameters={
                    "destination": "copy.txt",
                },
            )
        )


def test_copy_requires_destination():
    tool = CopyFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="copy_file",
                parameters={
                    "source": "source.txt",
                },
            )
        )


def test_copy_rejects_empty_parameters():
    tool = CopyFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="copy_file",
                parameters={
                    "source": "   ",
                    "destination": "copy.txt",
                },
            )
        )

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="copy_file",
                parameters={
                    "source": "source.txt",
                    "destination": "   ",
                },
            )
        )