from jaos_platform.base_platform_service import BasePlatformService
from jaos_platform.platform_runtime import PlatformRuntime


class DummyService(BasePlatformService):
    SERVICE_NAME = "dummy_service"


def test_base_service_registration():
    runtime = PlatformRuntime()

    service = DummyService(runtime)

    assert runtime.container.resolve("dummy_service") is service


def test_base_service_context():
    runtime = PlatformRuntime()

    DummyService(runtime)

    assert (
        runtime.context.get("dummy_service_status")
        == "READY"
    )