from kernel.jaos_kernel import JAOSKernel
from kernel.kernel_event_bus import KernelEventBus
from kernel.kernel_health_monitor import KernelHealthMonitor
from kernel.kernel_lifecycle_manager import KernelLifecycleManager
from kernel.kernel_permission_gateway import KernelPermissionGateway
from kernel.kernel_router import KernelRouter
from kernel.kernel_service_registry import KernelServiceRegistry
from kernel.runtime_context import RuntimeContext

print("\n========== JAOS KERNEL TEST ==========\n")

kernel = JAOSKernel()
kernel.start()

services = KernelServiceRegistry()
services.register_service("Configuration Service")
services.register_service("Logging Service")
services.register_service("Security Service")

events = KernelEventBus()
events.publish_event(
    "Kernel",
    "STARTUP",
    "Kernel initialized successfully."
)

lifecycle = KernelLifecycleManager()
lifecycle.register_platform("Memory Platform")
lifecycle.register_platform("Security Platform")
lifecycle.start_platform("Memory Platform")
lifecycle.start_platform("Security Platform")

health = KernelHealthMonitor()
health.update_status(
    "Memory Platform",
    "HEALTHY"
)
health.update_status(
    "Security Platform",
    "HEALTHY"
)

router = KernelRouter()
router.register_route(
    "MEMORY_UPDATED",
    "Memory Platform"
)
router.register_route(
    "PERMISSION_GRANTED",
    "Security Platform"
)

gateway = KernelPermissionGateway()
gateway.grant_permission(
    "OPEN_VSCODE"
)
gateway.revoke_permission(
    "DELETE_SYSTEM_FILES"
)

context = RuntimeContext()
context.update_context(
    "current_user",
    "Vinay"
)
context.update_context(
    "active_project",
    "JAOS"
)
context.update_context(
    "active_ai_provider",
    "OpenAI"
)

print("\n========== SUMMARY ==========\n")

services.show_services()
events.show_events()
lifecycle.show_status()
health.show_health()
router.show_routes()
gateway.show_permissions()
context.show_context()

print("\n========== JAOS KERNEL COMPLETE ==========")