from infrastructure.ai_provider_manager import AIProviderManager
from jaos_platform.platform_runtime import PlatformRuntime


def test_ai_provider_manager_registers_with_runtime():
    runtime = PlatformRuntime()

    manager = AIProviderManager(runtime)

    assert runtime.container.resolve("ai_provider_manager") is manager


def test_ai_provider_manager_updates_runtime_context():
    runtime = PlatformRuntime()

    AIProviderManager(runtime)

    assert runtime.context.get("ai_provider_manager_status") == "READY"


def test_ai_provider_registration_still_works():
    runtime = PlatformRuntime()

    manager = AIProviderManager(runtime)
    manager.register_provider("ollama", "AVAILABLE")

    assert manager.provider_status("ollama") == "AVAILABLE"