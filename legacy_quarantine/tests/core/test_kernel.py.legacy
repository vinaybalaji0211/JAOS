from core.kernel import JAOSKernel


def test_kernel_initial_state():
    kernel = JAOSKernel()

    assert kernel.system_status == "OFFLINE"
    assert kernel.registry_manager is None


def test_kernel_boot():
    kernel = JAOSKernel()

    assert kernel.boot() is True
    assert kernel.system_status == "ONLINE"
    assert kernel.registry_manager is not None


def test_kernel_status():
    kernel = JAOSKernel()

    kernel.boot()

    status = kernel.get_system_status()

    assert status["status"] == "ONLINE"
    assert status["registry_manager"] is True
    assert status["version"] == JAOSKernel.VERSION


def test_kernel_shutdown():
    kernel = JAOSKernel()

    kernel.boot()
    kernel.shutdown()

    assert kernel.system_status == "OFFLINE"