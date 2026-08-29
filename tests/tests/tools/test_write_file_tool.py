"""Canonical WriteFileTool requirements.

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
from jaos.tools.filesystem import WriteFileTool


def test_write_file_tool_metadata_contract():
    metadata = WriteFileTool().metadata()

    assert metadata.name == "write_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.write",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_WRITE,)
    assert metadata.approval_policy.level == ToolApprovalLevel.NONE
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_write_file_tool_requires_path():
    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={"content": "Hello JAOS"},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_write_file_tool_rejects_blank_path():
    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": "   ",
                "content": "Hello JAOS",
            },
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_write_file_tool_requires_content(tmp_path):
    file_path = tmp_path / "missing_content.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is False
    assert result.error == "Content must be a string."
    assert file_path.exists() is False


def test_write_file_tool_rejects_non_string_content(tmp_path):
    file_path = tmp_path / "numeric_content.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": 123,
            },
        )
    )

    assert result.success is False
    assert result.error == "Content must be a string."
    assert file_path.exists() is False


def test_write_file_tool_writes_new_file(tmp_path):
    file_path = tmp_path / "output.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Hello JAOS",
            },
        )
    )

    assert result.success is True
    assert result.error is None
    assert result.output == {
        "path": str(file_path),
        "bytes_written": 10,
    }
    assert file_path.read_text(encoding="utf-8") == "Hello JAOS"


def test_write_file_tool_reports_utf8_byte_length(tmp_path):
    file_path = tmp_path / "multibyte.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "héllo",
            },
        )
    )

    assert result.success is True
    assert result.output["bytes_written"] == 6
    assert file_path.read_bytes() == "héllo".encode()


def test_write_file_tool_overwrites_existing_file(tmp_path):
    file_path = tmp_path / "existing.txt"
    file_path.write_text("Old Content", encoding="utf-8")

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "New",
            },
        )
    )

    assert result.success is True
    assert file_path.read_text(encoding="utf-8") == "New"


def test_write_file_tool_creates_parent_directories(tmp_path):
    file_path = tmp_path / "folder" / "nested" / "file.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Created",
            },
        )
    )

    assert result.success is True
    assert file_path.read_text(encoding="utf-8") == "Created"
    assert file_path.parent.is_dir()


def test_write_file_tool_writes_empty_content(tmp_path):
    file_path = tmp_path / "empty.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "",
            },
        )
    )

    assert result.success is True
    assert result.output["bytes_written"] == 0
    assert file_path.read_text(encoding="utf-8") == ""


def test_write_file_tool_returns_failure_for_directory_target(tmp_path):
    directory_path = tmp_path / "target_directory"
    directory_path.mkdir()

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(directory_path),
                "content": "Hello JAOS",
            },
        )
    )

    assert result.success is False
    assert result.error
    assert directory_path.is_dir()


def test_write_file_tool_executes_through_the_tool_platform(tmp_path):
    permissions = ToolPermissionManager(("filesystem.write",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(WriteFileTool())

    file_path = tmp_path / "managed.txt"

    result = manager.execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Manager Write",
            },
        )
    )

    assert result.success is True
    assert file_path.read_text(encoding="utf-8") == "Manager Write"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "write_file"
    assert records[0].success is True
    assert records[0].error is None


def test_write_file_tool_requires_granted_permission(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(WriteFileTool())

    file_path = tmp_path / "denied.txt"

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="write_file",
                payload={
                    "path": str(file_path),
                    "content": "Denied",
                },
            )
        )

    assert file_path.exists() is False

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.write"


def test_write_file_tool_confines_effects_to_the_disposable_root(
    tmp_path,
    protected_repository_state,
):
    file_path = tmp_path / "confined" / "output.txt"

    result = WriteFileTool().execute(
        ToolRequest(
            tool_name="write_file",
            payload={
                "path": str(file_path),
                "content": "Confined",
            },
        )
    )

    assert result.success is True
    assert Path(result.output["path"]).is_relative_to(tmp_path)
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    ) == [
        "confined",
        "confined/output.txt",
    ]
