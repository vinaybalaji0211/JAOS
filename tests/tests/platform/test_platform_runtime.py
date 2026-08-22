from jaos_platform.platform_runtime import PlatformRuntime


def test_runtime_services_registered():

    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    assert runtime.container.is_registered("service_container")
    assert runtime.container.is_registered("service_registry")
    assert runtime.container.is_registered("runtime_context")
    assert runtime.container.is_registered("event_bus")


def test_registry_contains_services():

    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    assert runtime.registry.is_registered("service_container")
    assert runtime.registry.is_registered("service_registry")
    assert runtime.registry.is_registered("runtime_context")
    assert runtime.registry.is_registered("event_bus")


def test_container_returns_same_instance():

    runtime = PlatformRuntime()
    runtime.initialize()
    runtime.start()

    context = runtime.container.resolve("runtime_context")

    assert context is runtime.context