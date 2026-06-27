from kernel.boot_manager import BootManager

boot = BootManager()

boot.register_step(
    "Load Configuration"
)

boot.register_step(
    "Initialize Logger"
)

boot.register_step(
    "Start Kernel"
)

boot.register_step(
    "Create Runtime Context"
)

boot.register_step(
    "Register Services"
)

boot.register_step(
    "Initialize Platforms"
)

boot.register_step(
    "Health Verification"
)

boot.boot()