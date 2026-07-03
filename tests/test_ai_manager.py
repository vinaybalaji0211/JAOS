import pytest

from jaos.ai import (
    AIGenerateRequest,
    AIManager,
    AIPlatformStatus,
    AIProviderConfig,
    AIProviderType,
    ContextItem,
    ContextType,
    MockProvider,
    ProviderManager,
    RoutingStrategy,
)


def build_manager() -> AIManager:
    provider_manager = ProviderManager()
    provider_manager.register_provider(
        MockProvider(),
        AIProviderConfig(
            name="mock",
            provider_type=AIProviderType.MOCK,
            default_model="mock-model",
        ),
        set_default=True,
    )
    provider_manager.initialize_provider("mock")
    return AIManager(provider_manager)


def test_ai_manager_generates_response_with_default_provider():
    ai_manager = build_manager()

    response = ai_manager.generate("Explain JAOS")

    assert response.text == "mock: [USER]\nExplain JAOS"
    assert response.metadata.provider == "mock"
    assert response.metadata.model == "mock-model"


def test_ai_manager_generates_response_from_request():
    ai_manager = build_manager()

    request = AIGenerateRequest(
        prompt="Explain provider abstraction",
        routing_strategy=RoutingStrategy.DEFAULT,
        metadata={"source": "unit-test"},
    )

    response = ai_manager.generate_from_request(request)

    assert response.text == "mock: [USER]\nExplain provider abstraction"
    assert response.metadata.provider == "mock"


def test_ai_manager_uses_context_sections():
    ai_manager = build_manager()

    ai_manager.get_context_manager().add_context(
        ContextItem(
            context_type=ContextType.MEMORY,
            content="JAOS is a modular AI operating system.",
            priority=100,
        )
    )

    response = ai_manager.generate("What is JAOS?")

    assert "JAOS is a modular AI operating system." in response.text
    assert "[USER]\nWhat is JAOS?" in response.text


def test_ai_manager_supports_explicit_provider_routing():
    ai_manager = build_manager()

    response = ai_manager.generate(
        "Use explicit mock provider",
        routing_strategy=RoutingStrategy.EXPLICIT,
        provider_name="mock",
    )

    assert response.metadata.provider == "mock"
    assert response.text == "mock: [USER]\nUse explicit mock provider"


def test_ai_manager_rejects_invalid_request_type():
    ai_manager = build_manager()

    with pytest.raises(TypeError):
        ai_manager.generate_from_request("invalid")  # type: ignore[arg-type]


def test_ai_generate_request_rejects_empty_prompt():
    with pytest.raises(ValueError):
        AIGenerateRequest(prompt="   ")


def test_ai_platform_status_reports_current_state():
    ai_manager = build_manager()

    ai_manager.get_context_manager().add_context(
        ContextItem(
            context_type=ContextType.USER,
            content="User prefers modular architecture.",
            priority=100,
        )
    )
    ai_manager.get_context_manager().add_conversation_turn(
        "user",
        "Continue JAOS development.",
    )

    status = ai_manager.get_status()

    assert isinstance(status, AIPlatformStatus)
    assert status.provider_count == 1
    assert status.default_provider == "mock"
    assert status.context_items == 1
    assert status.conversation_turns == 1