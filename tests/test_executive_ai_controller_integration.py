from jaos.ai import (
    AIManager,
    AIProviderConfig,
    AIProviderType,
    MockProvider,
    ProviderManager,
)
from jaos.executive.ai import ExecutiveAIGateway
from jaos.executive.controller import ExecutiveController
from jaos.tools.tool_manager import ToolManager


def build_ai_manager() -> AIManager:
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


def test_unknown_request_falls_back_to_ai_gateway():
    controller = ExecutiveController(
        ToolManager(),
        ai_gateway=ExecutiveAIGateway(build_ai_manager()),
    )

    response = controller.process("Explain JAOS AI gateway")

    assert response.success is True
    assert "Explain JAOS AI gateway" in response.message
    assert response.output["provider"] == "mock"
    assert response.output["model"] == "mock-model"


def test_unknown_request_without_ai_returns_default_unknown_response():
    controller = ExecutiveController(ToolManager())

    response = controller.process("Explain JAOS AI gateway")

    assert response.success is False
    assert response.message == "I don't know how to handle that request yet."


def test_controller_accepts_ai_manager_for_backward_compatibility():
    controller = ExecutiveController(
        ToolManager(),
        ai_manager=build_ai_manager(),
    )

    response = controller.process("Explain JAOS AI manager compatibility")

    assert response.success is True
    assert "Explain JAOS AI manager compatibility" in response.message
    assert response.output["provider"] == "mock"