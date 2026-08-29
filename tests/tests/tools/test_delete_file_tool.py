"""Canonical DeleteFileTool requirements.

FORTRESS-06D2A migrated these requirements off the retired
``executive_brain`` filesystem tools onto ``jaos.tools.filesystem``.
Deletion is destructive, so every case runs inside the pytest-owned
``tmp_path`` root and the approval boundary is proven rather than bypassed.
"""

from pathlib import Path

import pytest

from jaos.tools import (
    ToolApprovalError,
    ToolApprovalLevel,
    ToolCapability,
    ToolManager,
    ToolPermissionError,
    ToolPermissionManager,
    ToolRequest,
    ToolRiskLevel,
    ToolStatus,
)
from jaos.tools.filesystem import DeleteFileTool


def test_delete_file_tool_metadata_contract():
    metadata = DeleteFileTool().metadata()

    assert metadata.name == "delete_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.delete",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_DELETE,)
    assert metadata.approval_policy.level == ToolApprovalLevel.DANGEROUS
    assert metadata.approval_policy.requires_approval() is True
    assert metadata.approval_policy.reason == (
        "Deleting files permanently removes data."
    )
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_delete_file_tool_requires_path():
    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_delete_file_tool_rejects_blank_path():
    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": "   "},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_delete_file_tool_reports_missing_file(tmp_path):
    missing_file = tmp_path / "missing.txt"

    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(missing_file)},
        )
    )

    assert result.success is False
    assert result.error == f"File does not exist: {missing_file}"


def test_delete_file_tool_rejects_directory(tmp_path):
    directory_path = tmp_path / "keep_directory"
    directory_path.mkdir()

    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(directory_path)},
        )
    )

    assert result.success is False
    assert result.error == f"Path is not a file: {directory_path}"
    assert directory_path.is_dir()


def test_delete_file_tool_deletes_file_on_direct_execution(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert result.error is None
    assert result.output == {
        "path": str(file_path),
        "deleted": True,
    }
    assert file_path.exists() is False


def test_delete_file_tool_is_blocked_without_approval(tmp_path):
    permissions = ToolPermissionManager(("filesystem.delete",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(DeleteFileTool())

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    with pytest.raises(ToolApprovalError):
        manager.execute(
            ToolRequest(
                tool_name="delete_file",
                payload={"path": str(file_path)},
                approved=False,
            )
        )

    assert file_path.exists() is True

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "delete_file"
    assert records[0].success is False
    assert records[0].error == "Deleting files permanently removes data."


def test_delete_file_tool_deletes_when_approved(tmp_path):
    permissions = ToolPermissionManager(("filesystem.delete",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(DeleteFileTool())

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(file_path)},
            approved=True,
        )
    )

    assert result.success is True
    assert file_path.exists() is False

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "delete_file"
    assert records[0].success is True
    assert records[0].error is None


def test_delete_file_tool_permission_precedes_approval(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(DeleteFileTool())

    file_path = tmp_path / "sample.txt"
    file_path.write_text("Hello JAOS", encoding="utf-8")

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="delete_file",
                payload={"path": str(file_path)},
                approved=True,
            )
        )

    assert file_path.exists() is True

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.delete"


def test_delete_file_tool_confines_deletion_to_the_target(
    tmp_path,
    protected_repository_state,
):
    target = tmp_path / "nested" / "target.txt"
    sibling = tmp_path / "nested" / "sibling.txt"
    target.parent.mkdir()
    target.write_text("Delete me", encoding="utf-8")
    sibling.write_text("Keep me", encoding="utf-8")

    result = DeleteFileTool().execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(target)},
        )
    )

    assert result.success is True
    assert Path(result.output["path"]).is_relative_to(tmp_path)
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    ) == [
        "nested",
        "nested/sibling.txt",
    ]
    assert sibling.read_text(encoding="utf-8") == "Keep me"
