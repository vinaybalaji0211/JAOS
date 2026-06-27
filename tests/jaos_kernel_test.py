from kernel.jaos_kernel import JAOSKernel

kernel = JAOSKernel()

kernel.register_platform(
    "Memory Platform"
)

kernel.register_platform(
    "Security Platform"
)

kernel.register_platform(
    "Workflow Platform"
)

kernel.start()

kernel.show_platforms()