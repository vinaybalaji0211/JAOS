import pytest

from jaos.tools import (
    ToolApprovalError,
    ToolApprovalLevel,
    ToolCapability,
    ToolManager,
    ToolPermissionManager,
    ToolRequest,
)
from jaos.tools.filesystem import DeleteFileTool


def test_delete_file_tool_metadata():
    tool = DeleteFileTool()
    metadata = tool.metadata()

    assert metadata.name == "delete_file"
    assert metadata.version == "1.0.0"
    assert metadata.permissions == ("filesystem.delete",)
    assert metadata.capabilities == (
        ToolCapability.FILESYSTEM_DELETE,
    )
    assert metadata.approval_policy.level == ToolApprovalLevel.DANGEROUS


def test_delete_file_tool_requires_path():
    tool = DeleteFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            payload={},
        )
    )

    assert result.success is False
    assert result.error == "File path is required."


def test_delete_file_tool_rejects_missing_file(tmp_path):
    tool = DeleteFileTool()
    missing_file = tmp_path / "missing.txt"

    result = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(missing_file)},
        )
    )

    assert result.success is False
    assert "File does not exist" in result.error


def test_delete_file_tool_rejects_directory(tmp_path):
    tool = DeleteFileTool()

    result = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(tmp_path)},
        )
    )

    assert result.success is False
    assert "Path is not a file" in result.error


def test_delete_file_tool_deletes_file_direct_execution(tmp_path):
    tool = DeleteFileTool()
    file_path = tmp_path / "delete_me.txt"
    file_path.write_text("Delete me", encoding="utf-8")

    result = tool.execute(
        ToolRequest(
            tool_name="delete_file",
            payload={"path": str(file_path)},
        )
    )

    assert result.success is True
    assert file_path.exists() is False
    assert result.output["deleted"] is True


def test_delete_file_tool_manager_requires_approval(tmp_path):
    permissions = ToolPermissionManager(("filesystem.delete",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(DeleteFileTool())

    file_path = tmp_path / "delete_me.txt"
    file_path.write_text("Delete me", encoding="utf-8")

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


def test_delete_file_tool_manager_deletes_when_approved(tmp_path):
    permissions = ToolPermissionManager(("filesystem.delete",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(DeleteFileTool())

    file_path = tmp_path / "delete_me.txt"
    file_path.write_text("Delete me", encoding="utf-8")

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