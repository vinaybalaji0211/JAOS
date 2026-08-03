from kernel.kernel_service_registry import KernelServiceRegistry

registry = KernelServiceRegistry()

registry.register_service(
    "Configuration Service"
)

registry.register_service(
    "Logging Service"
)

registry.register_service(
    "Security Service"
)

registry.show_services()