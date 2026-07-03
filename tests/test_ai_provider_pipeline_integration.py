from jaos.ai import (
    AIProviderConfig,
    AIProviderType,
    AIRequest,
    MockProvider,
    ProviderManager,
    ProviderRouter,
    ResponseManager,
    RoutingRequest,
    RoutingStrategy,
)


def test_ai_provider_pipeline_end_to_end():
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

    router = ProviderRouter(provider_manager)
    response_manager = ResponseManager()

    provider_name = router.resolve_provider(
        RoutingRequest(strategy=RoutingStrategy.DEFAULT)
    )

    raw_response = provider_manager.generate(
        AIRequest(
            prompt="Explain JAOS provider abstraction",
            metadata={"source": "integration-test"},
        ),
        provider_name=provider_name,
    )

    parsed_response = response_manager.process(raw_response)
    provider_state = provider_manager.get_state("mock")

    assert provider_name == "mock"
    assert raw_response.provider == "mock"
    assert raw_response.model == "mock-model"
    assert parsed_response.text == "mock: Explain JAOS provider abstraction"
    assert parsed_response.metadata.provider == "mock"
    assert parsed_response.metadata.model == "mock-model"
    assert provider_state.request_count == 1
    assert provider_state.success_count == 1
    assert provider_state.failure_count == 0

    provider_manager.shutdown_provider("mock")