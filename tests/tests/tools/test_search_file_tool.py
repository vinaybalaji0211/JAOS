"""Canonical SearchFileTool requirements.

FORTRESS-06D2A migrated these requirements off the retired
``executive_brain`` filesystem tools onto ``jaos.tools.filesystem``.

The canonical contract names the search root ``root``, defaults the pattern
to ``*`` instead of demanding one, and bounds the result set with
``max_results``.
"""

from pathlib import Path

import pytest

from jaos.tools import (
    ToolApprovalLevel,
    ToolCapability,
    ToolManager,
    ToolPermissionError,
    ToolPermissionManager,
    ToolRequest,
    ToolRiskLevel,
    ToolStatus,
)
from jaos.tools.filesystem import SearchFileTool


def test_search_file_tool_metadata_contract():
    metadata = SearchFileTool().metadata()

    assert metadata.name == "search_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.search",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_SEARCH,)
    assert metadata.approval_policy.level == ToolApprovalLevel.NONE
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_search_file_tool_declares_documented_defaults():
    assert SearchFileTool.DEFAULT_PATTERN == "*"
    assert SearchFileTool.DEFAULT_MAX_RESULTS == 100


def test_search_file_tool_requires_root():
    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={"pattern": "*.txt"},
        )
    )

    assert result.success is False
    assert result.error == "Search root is required."


def test_search_file_tool_rejects_blank_root():
    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": "   ",
                "pattern": "*.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Search root is required."


def test_search_file_tool_rejects_blank_pattern(tmp_path):
    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "   ",
            },
        )
    )

    assert result.success is False
    assert result.error == "Search pattern is required."


@pytest.mark.parametrize("max_results", [0, -1, "5", None])
def test_search_file_tool_rejects_invalid_max_results(tmp_path, max_results):
    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.txt",
                "max_results": max_results,
            },
        )
    )

    assert result.success is False
    assert result.error == "max_results must be a positive integer."


def test_search_file_tool_reports_missing_root(tmp_path):
    missing_root = tmp_path / "missing"

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(missing_root),
                "pattern": "*.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == f"Root directory does not exist: {missing_root}"


def test_search_file_tool_rejects_file_as_root(tmp_path):
    file_path = tmp_path / "demo.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(file_path),
                "pattern": "*.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == f"Root path is not a directory: {file_path}"


def test_search_file_tool_finds_matching_files(tmp_path):
    (tmp_path / "one.txt").write_text("A", encoding="utf-8")
    (tmp_path / "two.txt").write_text("B", encoding="utf-8")
    (tmp_path / "three.py").write_text("print()", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.txt",
            },
        )
    )

    assert result.success is True
    assert result.error is None
    assert result.output["root"] == str(tmp_path.resolve())
    assert result.output["pattern"] == "*.txt"
    assert result.output["count"] == 2
    assert sorted(Path(match).name for match in result.output["matches"]) == [
        "one.txt",
        "two.txt",
    ]


def test_search_file_tool_searches_recursively(tmp_path):
    nested = tmp_path / "folder" / "inner"
    nested.mkdir(parents=True)
    (nested / "demo.txt").write_text("Nested", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.txt",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 1
    assert result.output["matches"] == [str((nested / "demo.txt").resolve())]


def test_search_file_tool_returns_an_empty_result_set(tmp_path):
    (tmp_path / "one.txt").write_text("A", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.pdf",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 0
    assert result.output["matches"] == []


def test_search_file_tool_defaults_the_pattern_to_every_file(tmp_path):
    nested = tmp_path / "folder"
    nested.mkdir()
    (tmp_path / "one.txt").write_text("A", encoding="utf-8")
    (nested / "two.py").write_text("print()", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={"root": str(tmp_path)},
        )
    )

    assert result.success is True
    assert result.output["pattern"] == "*"
    assert result.output["count"] == 2
    assert sorted(Path(match).name for match in result.output["matches"]) == [
        "one.txt",
        "two.py",
    ]


def test_search_file_tool_excludes_directories_from_matches(tmp_path):
    (tmp_path / "match_directory").mkdir()
    (tmp_path / "match_file").write_text("A", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "match_*",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 1
    assert result.output["matches"] == [str((tmp_path / "match_file").resolve())]


def test_search_file_tool_caps_results_at_max_results(tmp_path):
    for index in range(5):
        (tmp_path / f"file_{index}.txt").write_text("A", encoding="utf-8")

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.txt",
                "max_results": 2,
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 2
    assert len(result.output["matches"]) == 2


def test_search_file_tool_executes_through_the_tool_platform(tmp_path):
    permissions = ToolPermissionManager(("filesystem.search",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(SearchFileTool())

    (tmp_path / "notes.md").write_text("# JAOS", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*.md",
            },
        )
    )

    assert result.success is True
    assert result.output["count"] == 1

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "search_file"
    assert records[0].success is True
    assert records[0].error is None


def test_search_file_tool_requires_granted_permission(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(SearchFileTool())

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="search_file",
                payload={
                    "root": str(tmp_path),
                    "pattern": "*.txt",
                },
            )
        )

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.search"


def test_search_file_tool_confines_results_to_the_disposable_root(tmp_path):
    (tmp_path / "one.txt").write_text("A", encoding="utf-8")

    before = sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    )

    result = SearchFileTool().execute(
        ToolRequest(
            tool_name="search_file",
            payload={
                "root": str(tmp_path),
                "pattern": "*",
            },
        )
    )

    after = sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    )

    assert result.success is True
    assert after == before
    assert Path(result.output["root"]).is_relative_to(tmp_path.resolve())
    for match in result.output["matches"]:
        assert Path(match).is_relative_to(tmp_path.resolve())
