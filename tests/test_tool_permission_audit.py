import pytest

from jaos.tools import (
    ToolAuditLogger,
    ToolAuditRecord,
    ToolInterface,
    ToolManager,
    ToolMetadata,
    ToolPermissionError,
    ToolPermissionManager,
    ToolRequest,
    ToolResult,
)


class SecureEchoTool(ToolInterface):
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="secure_echo",
            version="1.0.0",
            description="Secure echo test tool",
            permissions=("tool.echo",),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(success=True, output=request.payload)


class FailingTool(ToolInterface):
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="failing",
            version="1.0.0",
            description="Failing test tool",
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        raise RuntimeError("forced failure")


def test_permission_manager_lists_permissions():
    manager = ToolPermissionManager(("tool.echo",))

    assert manager.list_permissions() == ("tool.echo",)


def test_permission_manager_grant_and_revoke():
    manager = ToolPermissionManager()

    manager.grant("tool.echo")

    assert manager.list_permissions() == ("tool.echo",)

    manager.revoke("tool.echo")

    assert manager.list_permissions() == ()


def test_permission_manager_rejects_empty_grant():
    manager = ToolPermissionManager()

    with pytest.raises(ValueError):
        manager.grant(" ")


def test_permission_manager_authorizes_allowed_tool():
    permissions = ToolPermissionManager(("tool.echo",))
    metadata = ToolMetadata(
        name="secure_echo",
        version="1.0.0",
        description="Secure echo",
        permissions=("tool.echo",),
    )

    permissions.authorize(metadata)


def test_permission_manager_rejects_missing_permission():
    permissions = ToolPermissionManager()
    metadata = ToolMetadata(
        name="secure_echo",
        version="1.0.0",
        description="Secure echo",
        permissions=("tool.echo",),
    )

    with pytest.raises(ToolPermissionError):
        permissions.authorize(metadata)


def test_audit_record_rejects_empty_tool_name():
    with pytest.raises(ValueError):
        ToolAuditRecord(tool_name=" ", success=True)


def test_audit_logger_records_events():
    logger = ToolAuditLogger()
    record = ToolAuditRecord(tool_name="tool", success=True)

    logger.record(record)

    assert logger.list_records() == (record,)


def test_tool_manager_blocks_missing_permission_and_audits():
    manager = ToolManager()
    manager.register_tool(SecureEchoTool())

    with pytest.raises(ToolPermissionError):
        manager.execute(ToolRequest(tool_name="secure_echo"))

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "secure_echo"
    assert records[0].success is False
    assert "Missing tool permissions" in records[0].error


def test_tool_manager_executes_with_permission_and_audits_success():
    permissions = ToolPermissionManager(("tool.echo",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(SecureEchoTool())

    result = manager.execute(
        ToolRequest(
            tool_name="secure_echo",
            payload={"message": "hello"},
        )
    )

    records = manager.list_audit_records()

    assert result.success is True
    assert records[-1].tool_name == "secure_echo"
    assert records[-1].success is True


def test_tool_manager_audits_execution_failure():
    manager = ToolManager()
    manager.register_tool(FailingTool())

    with pytest.raises(RuntimeError):
        manager.execute(ToolRequest(tool_name="failing"))

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "failing"
    assert records[0].success is False
    assert records[0].error == "forced failure"