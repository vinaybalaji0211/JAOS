import pytest

from jaos.ai.provider import (
    AIProviderConfig,
    AIProviderGenerationError,
    AIProviderType,
    AIRequest,
    AIResponse,
    ProviderManager,
    ProviderManagerError,
)
from jaos.ai.providers.mock_provider import MockProvider


class TrackingMockProvider(MockProvider):
    def __init__(self) -> None:
        super().__init__()
        self.generate_calls = 0

    def generate(self, request: AIRequest) -> AIResponse:
        self.generate_calls += 1
        return super().generate(request)


def _configured_manager() -> tuple[ProviderManager, TrackingMockProvider]:
    manager = ProviderManager()
    provider = TrackingMockProvider()
    manager.register_provider(
        provider,
        AIProviderConfig(name="mock", provider_type=AIProviderType.MOCK),
    )
    return manager, provider


def test_ai_request_rejects_blank_and_whitespace_prompts() -> None:
    for prompt in ("", " \t\n"):
        with pytest.raises(ValueError):
            AIRequest(prompt=prompt)


def test_provider_manager_rejects_invalid_request_before_execution() -> None:
    manager, provider = _configured_manager()

    with pytest.raises(TypeError):
        manager.generate("not-an-ai-request")  # type: ignore[arg-type]

    state = manager.get_state("mock")
    assert provider.generate_calls == 0
    assert state.request_count == 0
    assert state.success_count == 0
    assert state.failure_count == 0
    assert state.last_error is None


def test_provider_manager_normalizes_generation_failure_and_records_state() -> None:
    manager, provider = _configured_manager()
    manager.initialize_provider("mock")

    with pytest.raises(ProviderManagerError) as error:
        manager.generate(AIRequest(prompt="fail"))

    state = manager.get_state("mock")
    assert provider.generate_calls == 1
    assert isinstance(error.value.__cause__, AIProviderGenerationError)
    assert state.request_count == 1
    assert state.success_count == 0
    assert state.failure_count == 1
    assert state.last_error == "Mock provider forced failure"
