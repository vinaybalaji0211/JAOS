from jaos.tools.tool_approval import ToolApprovalManager
from jaos.tools.tool_audit import ToolAuditLogger, ToolAuditRecord
from jaos.tools.tool_exceptions import ToolDisabledError
from jaos.tools.tool_interface import ToolInterface
from jaos.tools.tool_models import ToolRequest, ToolResult, ToolStatus
from jaos.tools.tool_permissions import ToolPermissionManager


class ToolExecutionEngine:
    """
    Responsible for executing tools.

    The execution engine performs:
    - Permission validation
    - Approval validation
    - Tool execution
    - Audit logging
    """

    def __init__(
        self,
        permissions: ToolPermissionManager,
        audit_logger: ToolAuditLogger,
        approval_manager: ToolApprovalManager | None = None,
    ) -> None:
        self._permissions = permissions
        self._audit_logger = audit_logger
        self._approval_manager = approval_manager or ToolApprovalManager()

    def execute(
        self,
        tool: ToolInterface,
        request: ToolRequest,
    ) -> ToolResult:
        metadata = tool.metadata()

        if metadata.status != ToolStatus.AVAILABLE:
            self._audit_logger.record(
                ToolAuditRecord(
                    tool_name=metadata.name,
                    success=False,
                    error="Tool is not available",
                )
            )
            raise ToolDisabledError(f"Tool is not available: {metadata.name}")

        try:
            self._permissions.authorize(metadata)
            self._approval_manager.require_approval(
                policy=metadata.approval_policy,
                approved=request.approved,
            )

            result = tool.execute(request)

            self._audit_logger.record(
                ToolAuditRecord(
                    tool_name=metadata.name,
                    success=result.success,
                    error=result.error,
                )
            )

            return result

        except Exception as exc:
            self._audit_logger.record(
                ToolAuditRecord(
                    tool_name=metadata.name,
                    success=False,
                    error=str(exc),
                )
            )
            raise