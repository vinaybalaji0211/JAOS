from kernel.boot_phase_manager import BootPhaseManager

manager = BootPhaseManager()

manager.register_step(
    "PRE_BOOT",
    "Load Configuration"
)

manager.register_step(
    "CORE_BOOT",
    "Initialize Logger"
)

manager.register_step(
    "KERNEL_BOOT",
    "Start JAOS Kernel"
)

manager.register_step(
    "PLATFORM_BOOT",
    "Register Platforms"
)

manager.register_step(
    "SERVICE_BOOT",
    "Register Services"
)

manager.register_step(
    "READY",
    "JAOS Ready"
)

manager.run_boot()