"""Canonical ReadFileTool requirements.

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
from jaos.tools.filesystem import ReadFileTool


def test_read_file_tool_metadata_contract():
    metadata = ReadFileTool().metadata()

    assert metadata.name == "read_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.read",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_READ,)
    assert metadata.approval_policy.level == ToolApprovalLevel.NONE
    assert metadata.approval_policy.requires_approval() is False
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_read_file_tool_requires_path():
    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_read_file_tool_rejects_blank_path():
    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": "   "},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_read_file_tool_rejects_non_string_path():
    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": 123},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_read_file_tool_reports_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(missing_file)},
        )
    )

    assert result.success is False
    assert result.error == f"File does not exist: {missing_file}"
    assert result.output is None


def test_read_file_tool_rejects_directory(tmp_path):
    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(tmp_path)},
        )
    )

    assert result.success is False
    assert result.error == f"Path is not a file: {tmp_path}"


def test_read_file_tool_reads_utf8_text(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS\nsecond line\n", encoding="utf-8")

    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.error is None
    assert result.output == {
        "path": str(file_path),
        "content": "Hello JAOS\nsecond line\n",
    }


def test_read_file_tool_reads_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.output["content"] == ""


def test_read_file_tool_rejects_non_utf8_payload(tmp_path):
    file_path = tmp_path / "binary.bin"
    file_path.write_bytes(b"\xff\xfe\x00payload")

    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is False
    assert result.error == f"File is not valid UTF-8 text: {file_path}"


def test_read_file_tool_executes_through_the_tool_platform(tmp_path):
    permissions = ToolPermissionManager(("filesystem.read",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(ReadFileTool())

    file_path = tmp_path / "managed.txt"
    file_path.write_text("Hello through manager", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.output["content"] == "Hello through manager"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "read_file"
    assert records[0].success is True
    assert records[0].error is None


def test_read_file_tool_requires_granted_permission(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(ReadFileTool())

    file_path = tmp_path / "denied.txt"
    file_path.write_text("Hidden", encoding="utf-8")

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="read_file",
                payload={"path": str(file_path)},
            )
        )

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "read_file"
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.read"


def test_read_file_tool_does_not_mutate_the_disposable_root(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    before = sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    )

    result = ReadFileTool().execute(
        ToolRequest(
            tool_name="read_file",
            payload={"path": str(file_path)},
        )
    )

    after = sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    )

    assert result.success is True
    assert after == before
    assert Path(result.output["path"]).is_relative_to(tmp_path)
    assert file_path.read_text(encoding="utf-8") == "Hello JAOS"
