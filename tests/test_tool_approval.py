import pytest

from jaos.tools import (
    ToolApprovalError,
    ToolApprovalLevel,
    ToolApprovalManager,
    ToolApprovalPolicy,
    ToolInterface,
    ToolManager,
    ToolMetadata,
    ToolPermissionManager,
    ToolRequest,
    ToolResult,
)


class ApprovalRequiredTool(ToolInterface):
    def metadata(self) -> ToolMetadata:
        return ToolMetadata(
            name="approval_required",
            version="1.0.0",
            description="Tool requiring approval",
            permissions=("tool.approval",),
            approval_policy=ToolApprovalPolicy(
                level=ToolApprovalLevel.DANGEROUS,
                reason="Dangerous action requires approval.",
            ),
        )

    def execute(self, request: ToolRequest) -> ToolResult:
        return ToolResult(success=True, output="executed")


def test_approval_policy_none_does_not_require_approval():
    policy = ToolApprovalPolicy()

    assert policy.requires_approval() is False


def test_approval_policy_dangerous_requires_approval():
    policy = ToolApprovalPolicy(level=ToolApprovalLevel.DANGEROUS)

    assert policy.requires_approval() is True


def test_approval_manager_allows_when_not_required():
    manager = ToolApprovalManager()
    policy = ToolApprovalPolicy()

    manager.require_approval(policy=policy, approved=False)


def test_approval_manager_blocks_when_required_and_not_approved():
    manager = ToolApprovalManager()
    policy = ToolApprovalPolicy(
        level=ToolApprovalLevel.DANGEROUS,
        reason="Dangerous action requires approval.",
    )

    with pytest.raises(ToolApprovalError):
        manager.require_approval(policy=policy, approved=False)


def test_approval_manager_allows_when_required_and_approved():
    manager = ToolApprovalManager()
    policy = ToolApprovalPolicy(level=ToolApprovalLevel.DANGEROUS)

    manager.require_approval(policy=policy, approved=True)


def test_tool_manager_blocks_unapproved_dangerous_tool():
    permissions = ToolPermissionManager(("tool.approval",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(ApprovalRequiredTool())

    with pytest.raises(ToolApprovalError):
        manager.execute(
            ToolRequest(
                tool_name="approval_required",
                approved=False,
            )
        )

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "approval_required"
    assert records[0].success is False
    assert records[0].error == "Dangerous action requires approval."


def test_tool_manager_allows_approved_dangerous_tool():
    permissions = ToolPermissionManager(("tool.approval",))
    manager = ToolManager(permissions=permissions)
    manager.register_tool(ApprovalRequiredTool())

    result = manager.execute(
        ToolRequest(
            tool_name="approval_required",
            approved=True,
        )
    )

    assert result.success is True
    assert result.output == "executed"

    records = manager.list_audit_records()

    assert len(records) == 1
    assert records[0].tool_name == "approval_required"
    assert records[0].success is True