import pytest

from jaos.ai.provider import (
    AIProvider,
    AIProviderCapabilities,
    AIProviderConfig,
    AIProviderHealth,
    AIProviderHealthStatus,
    AIProviderInfo,
    AIProviderLifecycleState,
    AIProviderType,
    AIRequest,
    AIResponse,
    ProviderDisabledError,
    ProviderManager,
    ProviderManagerError,
)


class MockProvider(AIProvider):
    def __init__(self, *, fail_initialize=False, fail_generate=False, healthy=True):
        self.initialized = False
        self.shutdown_called = False
        self.fail_initialize = fail_initialize
        self.fail_generate = fail_generate
        self.healthy = healthy

    def initialize(self) -> None:
        if self.fail_initialize:
            raise RuntimeError("init failed")
        self.initialized = True

    def shutdown(self) -> None:
        self.shutdown_called = True
        self.initialized = False

    def generate(self, request: AIRequest) -> AIResponse:
        if self.fail_generate:
            raise RuntimeError("generation failed")
        return AIResponse(text=f"mock: {request.prompt}", provider="mock")

    def stream_generate(self, request: AIRequest):
        yield f"mock: {request.prompt}"

    def health(self) -> AIProviderHealth:
        if self.healthy:
            return AIProviderHealth(status=AIProviderHealthStatus.HEALTHY)
        return AIProviderHealth(
            status=AIProviderHealthStatus.UNAVAILABLE,
            message="offline",
        )

    def provider_info(self) -> AIProviderInfo:
        return AIProviderInfo(
            name="mock",
            version="1.0.0",
            models=("mock-model",),
            capabilities=AIProviderCapabilities(),
        )


def test_register_provider_creates_config_and_state():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(
        name="mock",
        provider_type=AIProviderType.MOCK,
        default_model="mock-model",
    )

    manager.register_provider(provider, config)

    assert manager.count() == 1
    assert manager.get_provider("mock") is provider
    assert manager.get_config("mock") is config
    assert manager.get_state("mock").name == "mock"
    assert manager.get_state("mock").current_model == "mock-model"


def test_initialize_provider():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    manager.initialize_provider("mock")

    state = manager.get_state("mock")

    assert provider.initialized is True
    assert state.lifecycle == AIProviderLifecycleState.INITIALIZED
    assert state.available is True
    assert state.healthy is True


def test_initialize_disabled_provider_fails():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(
        name="mock",
        provider_type=AIProviderType.MOCK,
        enabled=False,
    )

    manager.register_provider(provider, config)

    with pytest.raises(ProviderDisabledError):
        manager.initialize_provider("mock")


def test_initialize_failure_updates_state():
    manager = ProviderManager()
    provider = MockProvider(fail_initialize=True)
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)

    with pytest.raises(ProviderManagerError):
        manager.initialize_provider("mock")

    state = manager.get_state("mock")

    assert state.lifecycle == AIProviderLifecycleState.FAILED
    assert state.available is False
    assert state.healthy is False
    assert state.last_error == "init failed"


def test_shutdown_provider():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    manager.initialize_provider("mock")
    manager.shutdown_provider("mock")

    state = manager.get_state("mock")

    assert provider.shutdown_called is True
    assert state.lifecycle == AIProviderLifecycleState.SHUTDOWN
    assert state.available is False
    assert state.healthy is False


def test_health_check_healthy():
    manager = ProviderManager()
    provider = MockProvider(healthy=True)
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    health = manager.health_check("mock")

    state = manager.get_state("mock")

    assert health.status == AIProviderHealthStatus.HEALTHY
    assert state.healthy is True
    assert state.available is True


def test_health_check_unhealthy():
    manager = ProviderManager()
    provider = MockProvider(healthy=False)
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    health = manager.health_check("mock")

    state = manager.get_state("mock")

    assert health.status == AIProviderHealthStatus.UNAVAILABLE
    assert state.healthy is False
    assert state.available is False
    assert state.last_error == "offline"


def test_generate_with_default_provider():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    response = manager.generate(AIRequest(prompt="hello"))

    state = manager.get_state("mock")

    assert response.text == "mock: hello"
    assert response.provider == "mock"
    assert state.request_count == 1
    assert state.success_count == 1
    assert state.failure_count == 0
    assert state.last_latency_seconds is not None


def test_generate_with_named_provider():
    manager = ProviderManager()
    provider_a = MockProvider()
    provider_b = MockProvider()
    config_a = AIProviderConfig(name="provider-a", provider_type=AIProviderType.MOCK)
    config_b = AIProviderConfig(name="provider-b", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider_a, config_a)
    manager.register_provider(provider_b, config_b)

    response = manager.generate(AIRequest(prompt="hello"), provider_name="provider-b")

    assert response.text == "mock: hello"
    assert manager.get_state("provider-b").success_count == 1
    assert manager.get_state("provider-a").success_count == 0


def test_generate_failure_updates_state():
    manager = ProviderManager()
    provider = MockProvider(fail_generate=True)
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)

    with pytest.raises(ProviderManagerError):
        manager.generate(AIRequest(prompt="hello"))

    state = manager.get_state("mock")

    assert state.request_count == 1
    assert state.success_count == 0
    assert state.failure_count == 1
    assert state.last_error == "generation failed"


def test_generate_disabled_provider_fails():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(
        name="mock",
        provider_type=AIProviderType.MOCK,
        enabled=False,
    )

    manager.register_provider(provider, config)

    with pytest.raises(ProviderDisabledError):
        manager.generate(AIRequest(prompt="hello"))


def test_set_default_provider():
    manager = ProviderManager()
    provider_a = MockProvider()
    provider_b = MockProvider()

    manager.register_provider(
        provider_a,
        AIProviderConfig(name="provider-a", provider_type=AIProviderType.MOCK),
    )
    manager.register_provider(
        provider_b,
        AIProviderConfig(name="provider-b", provider_type=AIProviderType.MOCK),
    )

    manager.set_default_provider("provider-b")

    assert manager.get_default_provider_name() == "provider-b"


def test_unregister_provider_removes_config_and_state():
    manager = ProviderManager()
    provider = MockProvider()
    config = AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK)

    manager.register_provider(provider, config)
    removed = manager.unregister_provider("mock")

    assert removed is provider
    assert manager.count() == 0