import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.delete_file_tool import DeleteFileTool


def test_delete_file_tool_name():
    tool = DeleteFileTool()

    assert tool.tool_name == "delete_file"


def test_delete_existing_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    tool = DeleteFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            parameters={"path": str(file_path)},
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File deleted successfully"
    assert not file_path.exists()
    assert response.data["path"] == str(file_path)


def test_delete_missing_file(tmp_path):
    file_path = tmp_path / "missing.txt"

    tool = DeleteFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            parameters={"path": str(file_path)},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "File does not exist"


def test_delete_directory_fails(tmp_path):
    tool = DeleteFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            parameters={"path": str(tmp_path)},
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Path is not a file"


def test_delete_requires_tool_request():
    tool = DeleteFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_delete_requires_path():
    tool = DeleteFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="delete_file",
                parameters={},
            )
        )


def test_delete_rejects_empty_path():
    tool = DeleteFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="delete_file",
                parameters={"path": "   "},
            )
        )