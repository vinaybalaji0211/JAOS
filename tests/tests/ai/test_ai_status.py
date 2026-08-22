from jaos.ai.diagnostics.ai_status import AIStatusProvider
from jaos.ai.provider import (
    AIProvider,
    AIProviderCapabilities,
    AIProviderConfig,
    AIProviderHealth,
    AIProviderHealthStatus,
    AIProviderInfo,
    AIProviderType,
    AIRequest,
    AIResponse,
    ProviderManager,
)


class FakeAIProvider(AIProvider):
    def __init__(self, *, health_status=AIProviderHealthStatus.HEALTHY):
        self.health_status = health_status

    def initialize(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(text="fake", provider="fake")

    def stream_generate(self, request: AIRequest):
        yield "fake"

    def health(self) -> AIProviderHealth:
        return AIProviderHealth(status=self.health_status)

    def provider_info(self) -> AIProviderInfo:
        return AIProviderInfo(
            name="fake",
            version="1.0.0",
            models=("fake-model",),
            capabilities=AIProviderCapabilities(),
        )


def test_status_reports_unhealthy_with_no_registered_providers():
    manager = ProviderManager()

    status = AIStatusProvider(manager).get_status()

    assert status.healthy is False
    assert status.details["provider_count"] == 0


def test_status_reports_healthy_when_default_provider_is_healthy():
    manager = ProviderManager()
    manager.register_provider(
        FakeAIProvider(health_status=AIProviderHealthStatus.HEALTHY),
        AIProviderConfig(name="fake", provider_type=AIProviderType.MOCK),
    )

    status = AIStatusProvider(manager).get_status()

    assert status.healthy is True


def test_status_reports_unhealthy_when_default_provider_is_unavailable():
    manager = ProviderManager()
    manager.register_provider(
        FakeAIProvider(health_status=AIProviderHealthStatus.UNAVAILABLE),
        AIProviderConfig(name="fake", provider_type=AIProviderType.MOCK),
    )

    status = AIStatusProvider(manager).get_status()

    assert status.healthy is False
    assert "unavailable" in status.message


def test_status_reports_unhealthy_when_health_check_raises():
    manager = ProviderManager()

    class BrokenProvider(FakeAIProvider):
        def health(self):
            raise RuntimeError("provider exploded")

    manager.register_provider(
        BrokenProvider(),
        AIProviderConfig(name="broken", provider_type=AIProviderType.MOCK),
    )

    status = AIStatusProvider(manager).get_status()

    assert status.healthy is False
