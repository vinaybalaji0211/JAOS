from brain.action_execution_engine import ActionExecutionEngine
from brain.tool_audit_logger import ToolAuditLogger
from brain.tool_core import ToolCore
from brain.tool_permission_manager import ToolPermissionManager
from brain.tool_registry import ToolRegistry
from brain.tool_routing_engine import ToolRoutingEngine

print(
    "\n=== TOOL & ACTION INTEGRATION TEST ===\n"
)

# Tool Core

core = ToolCore()

core.register_tool(
    "WebSearch",
    "Searches the internet"
)

core.show_tools()

# Tool Registry

registry = ToolRegistry()

registry.register(
    "WebSearch",
    "INTERNET",
    "Searches the web"
)

registry.show_registry()

# Permissions

permissions = (
    ToolPermissionManager()
)

permissions.register_tool(
    "WebSearch",
    False
)

permissions.register_tool(
    "DeleteFile",
    True
)

permissions.show_permissions()

# Routing

router = (
    ToolRoutingEngine()
)

router.register_route(
    "WEB_SEARCH",
    "WebSearch"
)

router.show_routes()

print(
    "Selected Tool:",
    router.get_tool(
        "WEB_SEARCH"
    )
)

# Execution

executor = (
    ActionExecutionEngine()
)

result = executor.execute(
    "WebSearch",
    "Search completed"
)

print(
    "Execution Result:",
    result
)

executor.show_history()

# Audit

audit = (
    ToolAuditLogger()
)

audit.log_action(
    "WebSearch",
    "Search AI research papers"
)

audit.show_logs()

print(
    "\n=== TOOL & ACTION SYSTEM COMPLETE ==="
)