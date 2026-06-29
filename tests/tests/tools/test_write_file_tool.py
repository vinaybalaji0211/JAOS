import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.write_file_tool import WriteFileTool


def test_write_file_tool_name():
    tool = WriteFileTool()

    assert tool.tool_name == "write_file"


def test_write_new_file(tmp_path):
    file_path = tmp_path / "output.txt"

    tool = WriteFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="write_file",
            parameters={
                "path": str(file_path),
                "content": "Hello JAOS",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.message == "File written successfully"

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "Hello JAOS"

    assert response.data["path"] == str(file_path)
    assert response.data["size"] == len("Hello JAOS")


def test_write_overwrite_existing_file(tmp_path):
    file_path = tmp_path / "existing.txt"
    file_path.write_text("Old Content", encoding="utf-8")

    tool = WriteFileTool()

    tool.execute(
        ToolRequest(
            tool_name="write_file",
            parameters={
                "path": str(file_path),
                "content": "New Content",
            },
        )
    )

    assert file_path.read_text(encoding="utf-8") == "New Content"


def test_write_creates_parent_directory(tmp_path):
    file_path = tmp_path / "folder" / "nested" / "file.txt"

    tool = WriteFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="write_file",
            parameters={
                "path": str(file_path),
                "content": "Created",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == "Created"


def test_write_requires_tool_request():
    tool = WriteFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_write_requires_path():
    tool = WriteFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="write_file",
                parameters={
                    "content": "Hello",
                },
            )
        )


def test_write_requires_content():
    tool = WriteFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="write_file",
                parameters={
                    "path": "demo.txt",
                },
            )
        )


def test_write_rejects_non_string_content():
    tool = WriteFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="write_file",
                parameters={
                    "path": "demo.txt",
                    "content": 123,
                },
            )
        )