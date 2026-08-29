"""Canonical CopyFileTool requirements.

FORTRESS-06D2A migrated these requirements off the retired
``executive_brain`` filesystem tools onto ``jaos.tools.filesystem``.
Every filesystem effect stays inside the pytest-owned ``tmp_path`` root.
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
from jaos.tools.filesystem import CopyFileTool


def test_copy_file_tool_metadata_contract():
    metadata = CopyFileTool().metadata()

    assert metadata.name == "copy_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.copy",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_COPY,)
    assert metadata.approval_policy.level == ToolApprovalLevel.NONE
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_copy_file_tool_requires_source():
    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={"destination": "copy.txt"},
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_copy_file_tool_rejects_blank_source():
    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": "   ",
                "destination": "copy.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_copy_file_tool_requires_destination(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={"source": str(source)},
        )
    )

    assert result.success is False
    assert result.error == "Destination path is required."


def test_copy_file_tool_rejects_blank_destination(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": "   ",
            },
        )
    )

    assert result.success is False
    assert result.error == "Destination path is required."


def test_copy_file_tool_reports_missing_source(tmp_path):
    source = tmp_path / "missing.txt"
    destination = tmp_path / "copy.txt"

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert result.error == f"Source file does not exist: {source}"
    assert destination.exists() is False


def test_copy_file_tool_rejects_directory_source(tmp_path):
    source = tmp_path / "source_directory"
    source.mkdir()
    destination = tmp_path / "copy.txt"

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert result.error == f"Source path is not a file: {source}"
    assert destination.exists() is False


def test_copy_file_tool_rejects_directory_destination(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")
    destination = tmp_path / "destination_directory"
    destination.mkdir()

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is False
    assert result.error == f"Destination path is a directory: {destination}"
    assert list(destination.iterdir()) == []


def test_copy_file_tool_copies_file_and_preserves_source(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert result.error is None
    assert result.output == {
        "source": str(source),
        "destination": str(destination),
    }
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"
    assert source.read_text(encoding="utf-8") == "Hello JAOS"


def test_copy_file_tool_creates_destination_directories(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "folder" / "copy.txt"
    source.write_text("Created", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert destination.read_text(encoding="utf-8") == "Created"


def test_copy_file_tool_overwrites_an_existing_destination_file(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("New Content", encoding="utf-8")
    destination.write_text("Old Content", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert destination.read_text(encoding="utf-8") == "New Content"
    assert source.read_text(encoding="utf-8") == "New Content"


def test_copy_file_tool_executes_through_the_tool_platform(tmp_path):
    permissions = ToolPermissionManager(("filesystem.copy",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(CopyFileTool())

    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("Manager Copy", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert destination.read_text(encoding="utf-8") == "Manager Copy"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "copy_file"
    assert records[0].success is True
    assert records[0].error is None


def test_copy_file_tool_requires_granted_permission(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(CopyFileTool())

    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("Denied", encoding="utf-8")

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="copy_file",
                payload={
                    "source": str(source),
                    "destination": str(destination),
                },
            )
        )

    assert destination.exists() is False

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.copy"


def test_copy_file_tool_confines_effects_to_the_disposable_root(
    tmp_path,
    protected_repository_state,
):
    source = tmp_path / "source.txt"
    destination = tmp_path / "nested" / "copy.txt"
    source.write_text("Confined", encoding="utf-8")

    result = CopyFileTool().execute(
        ToolRequest(
            tool_name="copy_file",
            payload={
                "source": str(source),
                "destination": str(destination),
            },
        )
    )

    assert result.success is True
    assert Path(result.output["source"]).is_relative_to(tmp_path)
    assert Path(result.output["destination"]).is_relative_to(tmp_path)
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    ) == [
        "nested",
        "nested/copy.txt",
        "source.txt",
    ]
