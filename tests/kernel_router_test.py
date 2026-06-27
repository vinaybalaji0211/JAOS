from kernel.kernel_router import KernelRouter

router = KernelRouter()

router.register_route(
    "PERMISSION_GRANTED",
    "Security Platform"
)

router.register_route(
    "WORKFLOW_STARTED",
    "Workflow Platform"
)

router.register_route(
    "MEMORY_UPDATED",
    "Memory Platform"
)

router.show_routes()

print()

print(
    "Resolve:",
    router.resolve_route(
        "MEMORY_UPDATED"
    )
)