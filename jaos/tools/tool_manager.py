from jaos.tools.tool_approval import ToolApprovalManager
from jaos.tools.tool_audit import ToolAuditLogger, ToolAuditRecord
from jaos.tools.tool_execution import ToolExecutionEngine
from jaos.tools.tool_interface import ToolInterface
from jaos.tools.tool_models import ToolRequest, ToolResult
from jaos.tools.tool_permissions import ToolPermissionManager
from jaos.tools.tool_registry import ToolRegistry


class ToolManager:
    """
    Public facade for the Tool Platform.

    Responsibilities:
    - Register tools
    - Discover tools
    - Delegate execution

    Execution is handled by ToolExecutionEngine.
    """

    def __init__(
        self,
        registry: ToolRegistry | None = None,
        permissions: ToolPermissionManager | None = None,
        audit_logger: ToolAuditLogger | None = None,
        approval_manager: ToolApprovalManager | None = None,
    ) -> None:
        self._registry = registry or ToolRegistry()
        self._permissions = permissions or ToolPermissionManager()
        self._audit_logger = audit_logger or ToolAuditLogger()
        self._approval_manager = approval_manager or ToolApprovalManager()

        self._execution_engine = ToolExecutionEngine(
            permissions=self._permissions,
            audit_logger=self._audit_logger,
            approval_manager=self._approval_manager,
        )

    def register_tool(self, tool: ToolInterface) -> None:
        self._registry.register(tool)

    def execute(self, request: ToolRequest) -> ToolResult:
        tool = self._registry.get(request.tool_name)

        return self._execution_engine.execute(
            tool=tool,
            request=request,
        )

    def has_tool(self, name: str) -> bool:
        return self._registry.has(name)

    def list_tools(self) -> tuple[str, ...]:
        return self._registry.list_tools()

    def list_audit_records(self) -> tuple[ToolAuditRecord, ...]:
        return self._audit_logger.list_records()