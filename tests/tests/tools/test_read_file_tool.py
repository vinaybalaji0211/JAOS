import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.read_file_tool import ReadFileTool


def test_read_file_tool_name():
    tool = ReadFileTool()

    assert tool.tool_name == "read_file"


def test_read_existing_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    tool = ReadFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="read_file",
            parameters={"path": str(file_path)},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File read successfully"
    assert response.data["content"] == "Hello JAOS"


def test_read_missing_file(tmp_path):
    file_path = tmp_path / "missing.txt"

    tool = ReadFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="read_file",
            parameters={"path": str(file_path)},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "File does not exist"


def test_read_directory_fails(tmp_path):
    tool = ReadFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="read_file",
            parameters={"path": str(tmp_path)},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Path is not a file"


def test_read_requires_tool_request():
    tool = ReadFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_read_requires_path_parameter():
    tool = ReadFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="read_file",
                parameters={},
            )
        )


def test_read_rejects_empty_path():
    tool = ReadFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="read_file",
                parameters={"path": "   "},
            )
        )