"""Canonical RenameFileTool requirements.

FORTRESS-06D2A migrated these requirements off the retired
``executive_brain`` filesystem tools onto ``jaos.tools.filesystem``.

The canonical contract is narrower than the retired one: a rename takes a
bare ``new_name`` and can only rename a file inside its own directory. The
legacy ability to relocate a file into a newly created directory is not
preserved, and the containment rule is asserted instead.
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
from jaos.tools.filesystem import RenameFileTool


def test_rename_file_tool_metadata_contract():
    metadata = RenameFileTool().metadata()

    assert metadata.name == "rename_file"
    assert metadata.version == "1.0.0"
    assert metadata.description
    assert metadata.permissions == ("filesystem.rename",)
    assert metadata.capabilities == (ToolCapability.FILESYSTEM_RENAME,)
    assert metadata.approval_policy.level == ToolApprovalLevel.NONE
    assert metadata.risk_level == ToolRiskLevel.LOW
    assert metadata.status == ToolStatus.AVAILABLE


def test_rename_file_tool_requires_source():
    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={"new_name": "renamed.txt"},
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_rename_file_tool_rejects_blank_source():
    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": "   ",
                "new_name": "renamed.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "Source path is required."


def test_rename_file_tool_requires_new_name(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={"source": str(source)},
        )
    )

    assert result.success is False
    assert result.error == "New file name is required."
    assert source.exists() is True


def test_rename_file_tool_rejects_blank_new_name(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "   ",
            },
        )
    )

    assert result.success is False
    assert result.error == "New file name is required."
    assert source.exists() is True


def test_rename_file_tool_rejects_relative_path_as_new_name(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "nested/renamed.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == "New file name must not include a path."
    assert source.exists() is True
    assert (tmp_path / "nested").exists() is False


def test_rename_file_tool_rejects_absolute_path_as_new_name(tmp_path):
    source = tmp_path / "source.txt"
    outside = tmp_path / "outside" / "renamed.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": str(outside),
            },
        )
    )

    assert result.success is False
    assert result.error == "New file name must not include a path."
    assert source.exists() is True
    assert outside.parent.exists() is False


def test_rename_file_tool_rejects_parent_traversal_as_new_name(tmp_path):
    source = tmp_path / "nested" / "source.txt"
    source.parent.mkdir()
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "..",
            },
        )
    )

    assert result.success is False
    assert source.read_text(encoding="utf-8") == "Hello JAOS"


def test_rename_file_tool_reports_missing_source(tmp_path):
    source = tmp_path / "missing.txt"

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "renamed.txt",
            },
        )
    )

    assert result.success is False
    assert result.error == f"Source file does not exist: {source}"
    assert (tmp_path / "renamed.txt").exists() is False


def test_rename_file_tool_rejects_directory_source(tmp_path):
    source = tmp_path / "source_directory"
    source.mkdir()

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "renamed",
            },
        )
    )

    assert result.success is False
    assert result.error == f"Source path is not a file: {source}"
    assert source.is_dir()


def test_rename_file_tool_rejects_existing_destination(tmp_path):
    source = tmp_path / "source.txt"
    destination = tmp_path / "existing.txt"
    source.write_text("Hello JAOS", encoding="utf-8")
    destination.write_text("Existing", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": destination.name,
            },
        )
    )

    assert result.success is False
    assert result.error == f"Destination already exists: {destination}"
    assert source.read_text(encoding="utf-8") == "Hello JAOS"
    assert destination.read_text(encoding="utf-8") == "Existing"


def test_rename_file_tool_renames_within_the_source_directory(tmp_path):
    source = tmp_path / "nested" / "old_name.txt"
    source.parent.mkdir()
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "new_name.txt",
            },
        )
    )

    destination = source.parent / "new_name.txt"

    assert result.success is True
    assert result.error is None
    assert result.output == {
        "source": str(source),
        "destination": str(destination),
    }
    assert source.exists() is False
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"
    assert destination.parent == source.parent


def test_rename_file_tool_normalizes_surrounding_whitespace(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello JAOS", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "  renamed.txt  ",
            },
        )
    )

    destination = tmp_path / "renamed.txt"

    assert result.success is True
    assert result.output["destination"] == str(destination)
    assert destination.read_text(encoding="utf-8") == "Hello JAOS"


def test_rename_file_tool_executes_through_the_tool_platform(tmp_path):
    permissions = ToolPermissionManager(("filesystem.rename",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(RenameFileTool())

    source = tmp_path / "source.txt"
    source.write_text("Manager Rename", encoding="utf-8")

    result = manager.execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "managed.txt",
            },
        )
    )

    assert result.success is True
    renamed = tmp_path / "managed.txt"

    assert source.exists() is False
    assert renamed.read_text(encoding="utf-8") == "Manager Rename"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "rename_file"
    assert records[0].success is True
    assert records[0].error is None


def test_rename_file_tool_requires_granted_permission(tmp_path):
    manager = ToolManager(permissions=ToolPermissionManager())
    manager.register_tool(RenameFileTool())

    source = tmp_path / "source.txt"
    source.write_text("Denied", encoding="utf-8")

    with pytest.raises(ToolPermissionError):
        manager.execute(
            ToolRequest(
                tool_name="rename_file",
                payload={
                    "source": str(source),
                    "new_name": "renamed.txt",
                },
            )
        )

    assert source.read_text(encoding="utf-8") == "Denied"
    assert (tmp_path / "renamed.txt").exists() is False

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].success is False
    assert records[0].error == "Missing tool permissions: filesystem.rename"


def test_rename_file_tool_confines_effects_to_the_disposable_root(
    tmp_path,
    protected_repository_state,
):
    source = tmp_path / "nested" / "source.txt"
    source.parent.mkdir()
    source.write_text("Confined", encoding="utf-8")

    result = RenameFileTool().execute(
        ToolRequest(
            tool_name="rename_file",
            payload={
                "source": str(source),
                "new_name": "renamed.txt",
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
        "nested/renamed.txt",
    ]
