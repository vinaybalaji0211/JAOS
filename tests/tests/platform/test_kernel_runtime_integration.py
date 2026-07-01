from kernel.jaos_kernel import JAOSKernel
from jaos_platform.platform_runtime import PlatformRuntime


def test_kernel_owns_platform_runtime():
    kernel = JAOSKernel()

    assert isinstance(kernel.runtime, PlatformRuntime)


def test_kernel_registers_platform_runtime():
    kernel = JAOSKernel()

    assert "platform_runtime" in kernel.platforms
    assert kernel.platforms["platform_runtime"]["status"] == "ACTIVE"


def test_kernel_start_updates_runtime_context():
    kernel = JAOSKernel()

    kernel.start()

    assert kernel.runtime.context.get("kernel_status") == "ONLINE"