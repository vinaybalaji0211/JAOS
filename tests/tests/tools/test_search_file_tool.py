import pytest

from executive_brain.tools.core.tool_models import (
    ToolRequest,
    ToolStatus,
)
from executive_brain.tools.file.search_file_tool import SearchFileTool


def test_search_file_tool_name():
    tool = SearchFileTool()

    assert tool.tool_name == "search_file"


def test_search_files_success(tmp_path):
    (tmp_path / "one.txt").write_text("A", encoding="utf-8")
    (tmp_path / "two.txt").write_text("B", encoding="utf-8")
    (tmp_path / "three.py").write_text("print()", encoding="utf-8")

    tool = SearchFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="search_file",
            parameters={
                "path": str(tmp_path),
                "pattern": "*.txt",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert len(response.data["matches"]) == 2

    assert any(path.endswith("one.txt") for path in response.data["matches"])
    assert any(path.endswith("two.txt") for path in response.data["matches"])


def test_search_nested_directories(tmp_path):
    nested = tmp_path / "folder" / "inner"
    nested.mkdir(parents=True)

    (nested / "demo.txt").write_text("Nested", encoding="utf-8")

    tool = SearchFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="search_file",
            parameters={
                "path": str(tmp_path),
                "pattern": "*.txt",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert len(response.data["matches"]) == 1
    assert response.data["matches"][0].endswith("demo.txt")


def test_search_returns_empty_result(tmp_path):
    tool = SearchFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="search_file",
            parameters={
                "path": str(tmp_path),
                "pattern": "*.pdf",
            },
        )
    )

    assert response.status == ToolStatus.SUCCESS
    assert response.data["matches"] == []


def test_search_missing_directory(tmp_path):
    tool = SearchFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="search_file",
            parameters={
                "path": str(tmp_path / "missing"),
                "pattern": "*.txt",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Search path does not exist"


def test_search_requires_directory(tmp_path):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("Hello", encoding="utf-8")

    tool = SearchFileTool()

    response = tool.execute(
        ToolRequest(
            tool_name="search_file",
            parameters={
                "path": str(file_path),
                "pattern": "*.txt",
            },
        )
    )

    assert response.status == ToolStatus.FAILURE
    assert response.message == "Search path is not a directory"


def test_search_requires_tool_request():
    tool = SearchFileTool()

    with pytest.raises(TypeError):
        tool.execute("invalid-request")


def test_search_requires_path():
    tool = SearchFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="search_file",
                parameters={
                    "pattern": "*.txt",
                },
            )
        )


def test_search_requires_pattern():
    tool = SearchFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="search_file",
                parameters={
                    "path": ".",
                },
            )
        )


def test_search_rejects_empty_values():
    tool = SearchFileTool()

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="search_file",
                parameters={
                    "path": "   ",
                    "pattern": "*.txt",
                },
            )
        )

    with pytest.raises(ValueError):
        tool.execute(
            ToolRequest(
                tool_name="search_file",
                parameters={
                    "path": ".",
                    "pattern": "   ",
                },
            )
        )