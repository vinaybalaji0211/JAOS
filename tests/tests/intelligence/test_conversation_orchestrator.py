"""Tests for end-to-end conversation orchestration."""

from datetime import datetime, timedelta, timezone

import pytest

from jaos.ai.ai_manager import AIManager
from jaos.ai.ai_models import AIGenerateRequest
from jaos.ai.prompt import CompiledPrompt
from jaos.ai.response.response_models import (
    ParsedResponse,
    ResponseMetadata,
)
from jaos.intelligence import (
    ContextBundle,
    ConversationRole,
    ConversationSessionState,
    ConversationTurn,
    IntelligenceConversationError,
    IntelligenceIdentity,
    IntelligencePermissionError,
    IntelligenceResultStatus,
    IntelligenceScope,
)
from jaos.intelligence.conversation.conversation_orchestrator import (
    ConversationOrchestrator,
)
from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_policy_registry import (
    ConversationPolicyRegistry,
)
from jaos.intelligence.conversation.conversation_reference_resolver import (
    ConversationReferenceResolver,
)
from jaos.intelligence.conversation.conversation_session_manager import (
    ConversationSessionManager,
)
from jaos.intelligence.conversation.in_memory_conversation_session_store import (
    InMemoryConversationSessionStore,
)
from jaos.intelligence.interfaces.prompt_composer import PromptComposer
from jaos.intelligence.models.intelligence_request_type import (
    IntelligenceRequestType,
)
from jaos.intelligence.prompt.prompt_composition_models import (
    PromptCompositionRequest,
    PromptCompositionResult,
)

BASE_TIME = datetime(2026, 7, 20, 12, 0, tzinfo=timezone.utc)


def fixed_clock() -> datetime:
    return BASE_TIME


def create_identity(
    identity_id: str = "vinay",
) -> IntelligenceIdentity:
    return IntelligenceIdentity(
        IntelligenceScope.USER,
        identity_id,
    )


def create_turn(
    *,
    session_id: str = "session-1",
    turn_id: str = "turn-1",
    role: ConversationRole = ConversationRole.USER,
    content: str = "Explain the JAOS architecture",
    created_at: datetime = BASE_TIME + timedelta(seconds=1),
) -> ConversationTurn:
    return ConversationTurn(
        session_id=session_id,
        role=role,
        content=content,
        source="user",
        turn_id=turn_id,
        created_at=created_at,
    )


def create_context_bundle(
    identity: IntelligenceIdentity,
    *,
    request_id: str = "request-1",
    context_policy: str | None = "default",
) -> ContextBundle:
    return ContextBundle(
        request_id=request_id,
        identity=identity,
        bundle_id=f"bundle-{request_id}",
        context_policy=context_policy,
    )


def create_parsed_response(
    *,
    text: str = "JAOS is ready.",
    provider: str = "mock",
    model: str | None = "mock-model",
    source_metadata: dict | None = None,
) -> ParsedResponse:
    metadata = (
        {"trace_id": "trace-1"}
        if source_metadata is None
        else source_metadata
    )

    return ParsedResponse(
        text=text,
        metadata=ResponseMetadata(
            provider=provider,
            model=model,
            source_metadata=metadata,
        ),
    )


class RecordingPromptComposer(PromptComposer):
    """Minimal ready-state prompt composer used at the public boundary."""

    def __init__(
        self,
        *,
        ready: bool = True,
        error: Exception | None = None,
    ) -> None:
        self._ready = ready
        self.error = error
        self.requests: list[PromptCompositionRequest] = []

    @property
    def component_name(self) -> str:
        return "recording-prompt-composer"

    @property
    def is_ready(self) -> bool:
        return self._ready

    def initialize(self) -> None:
        self._ready = True

    def shutdown(self) -> None:
        self._ready = False

    def compose(
        self,
        composition_request: PromptCompositionRequest,
    ) -> PromptCompositionResult:
        self.requests.append(composition_request)

        if self.error is not None:
            raise self.error

        context_item_ids = tuple(
            item.item_id
            for item in composition_request.context_bundle.items
        )

        return PromptCompositionResult(
            compiled_prompt=CompiledPrompt(
                text="COMPILED CONVERSATION PROMPT",
                section_count=1,
            ),
            template_reference="conversation@1.0",
            supplemental_sections=(),
            context_item_ids=context_item_ids,
            estimated_prompt_tokens=8,
            redacted_item_ids=(),
            contained_item_ids=(),
            metadata={"test_double": True},
        )


class RecordingAIManager(AIManager):
    """AIManager boundary double that never constructs provider internals."""

    def __init__(
        self,
        *,
        response: ParsedResponse | None = None,
        error: Exception | None = None,
    ) -> None:
        self.response = response or create_parsed_response()
        self.error = error
        self.requests: list[AIGenerateRequest] = []

    def generate_from_request(
        self,
        request: AIGenerateRequest,
    ) -> ParsedResponse:
        if not isinstance(request, AIGenerateRequest):
            raise TypeError(
                "request must be an AIGenerateRequest"
            )

        self.requests.append(request)

        if self.error is not None:
            raise self.error

        return self.response


def create_orchestrator(
    *,
    policy: ConversationPolicy | None = None,
    prompt_composer: RecordingPromptComposer | None = None,
    ai_manager: RecordingAIManager | None = None,
    initialize: bool = True,
) -> tuple[
    ConversationOrchestrator,
    ConversationSessionManager,
    RecordingPromptComposer,
    RecordingAIManager,
]:
    registry = ConversationPolicyRegistry()
    registry.register_policy(
        policy
        or ConversationPolicy(
            policy_name="default",
            context_policy="default",
        ),
        make_default=True,
    )

    session_manager = ConversationSessionManager(
        InMemoryConversationSessionStore(),
        registry,
        clock=fixed_clock,
    )
    resolved_prompt_composer = (
        prompt_composer or RecordingPromptComposer()
    )
    resolved_ai_manager = ai_manager or RecordingAIManager()

    orchestrator = ConversationOrchestrator(
        session_manager,
        registry,
        ConversationReferenceResolver(),
        resolved_prompt_composer,
        resolved_ai_manager,
        template_id="conversation",
        template_version="1.0",
    )

    if initialize:
        orchestrator.initialize()

    return (
        orchestrator,
        session_manager,
        resolved_prompt_composer,
        resolved_ai_manager,
    )


def start_known_session(
    session_manager: ConversationSessionManager,
    identity: IntelligenceIdentity,
) -> None:
    session_manager.start_session(
        identity,
        session_id="session-1",
    )


def test_orchestrator_requires_ready_prompt_composer() -> None:
    prompt_composer = RecordingPromptComposer(ready=False)
    orchestrator, _, _, _ = create_orchestrator(
        prompt_composer=prompt_composer,
        initialize=False,
    )

    with pytest.raises(
        IntelligenceConversationError,
        match="prompt composer must be initialized",
    ):
        orchestrator.initialize()

    prompt_composer.initialize()
    orchestrator.initialize()

    assert orchestrator.is_ready is True


def test_shutdown_rejects_new_work() -> None:
    orchestrator, _, _, _ = create_orchestrator()
    orchestrator.shutdown()

    with pytest.raises(
        IntelligenceConversationError,
        match="not initialized",
    ):
        orchestrator.start_session(create_identity())


def test_public_session_lifecycle() -> None:
    orchestrator, _, _, _ = create_orchestrator()

    session = orchestrator.start_session(
        create_identity(),
        metadata={"owner": "vinay"},
    )

    assert session.state is ConversationSessionState.ACTIVE
    assert session.metadata["owner"] == "vinay"
    assert orchestrator.get_session(session.session_id) == session

    closed = orchestrator.close_session(session.session_id)

    assert closed.state is ConversationSessionState.CLOSED
    assert orchestrator.get_session(session.session_id) == closed


def test_successful_turn_uses_ai_manager_boundary() -> None:
    orchestrator, session_manager, composer, ai_manager = (
        create_orchestrator()
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    user_turn = create_turn()
    result = orchestrator.process_turn(
        "session-1",
        user_turn,
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.SUCCEEDED
    assert result.output == "JAOS is ready."
    assert result.provider_name == "mock"
    assert result.provider_model == "mock-model"
    assert result.structured_output["session_id"] == "session-1"
    assert result.structured_output["user_turn_id"] == "turn-1"
    assert result.metadata["component"] == "conversation_orchestrator"

    assert len(composer.requests) == 1
    composition_request = composer.requests[0]
    assert composition_request.request.objective == user_turn.content
    assert (
        composition_request.request.request_type
        is IntelligenceRequestType.CONVERSATION
    )
    assert composition_request.request.identity == identity
    assert composition_request.request.session_id == "session-1"

    assert len(ai_manager.requests) == 1
    ai_request = ai_manager.requests[0]
    assert ai_request.prompt == "COMPILED CONVERSATION PROMPT"
    assert (
        ai_request.metadata["intelligence_request_id"]
        == "request-1"
    )
    assert (
        ai_request.metadata["conversation_session_id"]
        == "session-1"
    )
    assert ai_request.metadata["conversation_turn_id"] == "turn-1"

    final_session = session_manager.get_required_session("session-1")
    assert tuple(
        turn.role for turn in final_session.turns
    ) == (
        ConversationRole.USER,
        ConversationRole.ASSISTANT,
    )
    assert final_session.turns[0] == user_turn
    assert final_session.turns[1].content == "JAOS is ready."
    assert final_session.turns[1].source == "ai_provider"


def test_unresolved_reference_returns_clarification_without_provider() -> None:
    orchestrator, session_manager, composer, ai_manager = (
        create_orchestrator()
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(content="Continue that"),
        create_context_bundle(identity),
    )

    assert (
        result.status
        is IntelligenceResultStatus.REQUIRES_CLARIFICATION
    )
    assert result.output == (
        "I need clarification before I can safely resolve "
        "that reference."
    )
    assert result.metadata["provider_invoked"] is False
    assert composer.requests == []
    assert ai_manager.requests == []

    final_session = session_manager.get_required_session("session-1")
    assert tuple(
        turn.role for turn in final_session.turns
    ) == (
        ConversationRole.USER,
        ConversationRole.ASSISTANT,
    )
    assert (
        final_session.turns[-1].source
        == "conversation_orchestrator"
    )


def test_identity_mismatch_is_rejected_before_session_mutation() -> None:
    orchestrator, session_manager, composer, ai_manager = (
        create_orchestrator()
    )
    owner = create_identity("vinay")
    another_user = create_identity("another-user")
    start_known_session(session_manager, owner)

    with pytest.raises(
        IntelligencePermissionError,
        match="identity does not match",
    ):
        orchestrator.process_turn(
            "session-1",
            create_turn(),
            create_context_bundle(another_user),
        )

    assert (
        session_manager.get_required_session("session-1").turns
        == ()
    )
    assert composer.requests == []
    assert ai_manager.requests == []


def test_context_policy_mismatch_is_rejected() -> None:
    orchestrator, session_manager, composer, ai_manager = (
        create_orchestrator()
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    with pytest.raises(
        IntelligenceConversationError,
        match="policy does not match",
    ):
        orchestrator.process_turn(
            "session-1",
            create_turn(),
            create_context_bundle(
                identity,
                context_policy="strict",
            ),
        )

    assert (
        session_manager.get_required_session("session-1").turns
        == ()
    )
    assert composer.requests == []
    assert ai_manager.requests == []


def test_non_user_input_turn_is_rejected() -> None:
    orchestrator, session_manager, _, _ = create_orchestrator()
    identity = create_identity()
    start_known_session(session_manager, identity)

    with pytest.raises(
        IntelligenceConversationError,
        match="user role",
    ):
        orchestrator.process_turn(
            "session-1",
            create_turn(role=ConversationRole.ASSISTANT),
            create_context_bundle(identity),
        )


def test_prompt_composition_failure_returns_failed_result() -> None:
    composer = RecordingPromptComposer(
        error=RuntimeError("prompt composition failed"),
    )
    orchestrator, session_manager, _, ai_manager = (
        create_orchestrator(prompt_composer=composer)
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(),
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.FAILED
    assert result.error_code == "runtimeerror"
    assert result.error_message == "prompt composition failed"
    assert result.metadata["session_preserved"] is True
    assert len(composer.requests) == 1
    assert ai_manager.requests == []
    assert len(
        session_manager.get_required_session("session-1").turns
    ) == 1


def test_provider_failure_returns_failed_result() -> None:
    ai_manager = RecordingAIManager(
        error=RuntimeError("provider unavailable"),
    )
    orchestrator, session_manager, composer, _ = (
        create_orchestrator(ai_manager=ai_manager)
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(),
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.FAILED
    assert result.error_code == "runtimeerror"
    assert result.error_message == "provider unavailable"
    assert result.metadata["session_preserved"] is True
    assert len(composer.requests) == 1
    assert len(ai_manager.requests) == 1
    assert len(
        session_manager.get_required_session("session-1").turns
    ) == 1


def test_invalid_provider_response_returns_failed_result() -> None:
    ai_manager = RecordingAIManager(
        response=create_parsed_response(
            text="unsafe\x00response",
        ),
    )
    orchestrator, session_manager, _, _ = create_orchestrator(
        ai_manager=ai_manager,
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(),
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.FAILED
    assert result.error_code == "intelligenceconversationerror"
    assert "null character" in result.error_message
    assert len(
        session_manager.get_required_session("session-1").turns
    ) == 1


def test_policy_response_character_limit_is_enforced() -> None:
    policy = ConversationPolicy(
        policy_name="default",
        context_policy="default",
        max_provider_response_characters=5,
    )
    ai_manager = RecordingAIManager(
        response=create_parsed_response(text="123456"),
    )
    orchestrator, session_manager, _, _ = create_orchestrator(
        policy=policy,
        ai_manager=ai_manager,
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(),
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.FAILED
    assert "character limit" in result.error_message
    assert len(
        session_manager.get_required_session("session-1").turns
    ) == 1


def test_policy_response_metadata_limit_is_enforced() -> None:
    policy = ConversationPolicy(
        policy_name="default",
        context_policy="default",
        max_provider_metadata_items=1,
    )
    ai_manager = RecordingAIManager(
        response=create_parsed_response(
            source_metadata={
                "first": 1,
                "second": 2,
            },
        ),
    )
    orchestrator, session_manager, _, _ = create_orchestrator(
        policy=policy,
        ai_manager=ai_manager,
    )
    identity = create_identity()
    start_known_session(session_manager, identity)

    result = orchestrator.process_turn(
        "session-1",
        create_turn(),
        create_context_bundle(identity),
    )

    assert result.status is IntelligenceResultStatus.FAILED
    assert "metadata limit" in result.error_message
    assert len(
        session_manager.get_required_session("session-1").turns
    ) == 1


def test_closed_session_rejects_new_turn() -> None:
    orchestrator, session_manager, composer, ai_manager = (
        create_orchestrator()
    )
    identity = create_identity()
    start_known_session(session_manager, identity)
    orchestrator.close_session("session-1")

    with pytest.raises(
        IntelligenceConversationError,
        match="invalid state",
    ):
        orchestrator.process_turn(
            "session-1",
            create_turn(),
            create_context_bundle(identity),
        )

    assert composer.requests == []
    assert ai_manager.requests == []


def test_process_turn_rejects_invalid_argument_types() -> None:
    orchestrator, _, _, _ = create_orchestrator()

    with pytest.raises(
        TypeError,
        match="ConversationTurn",
    ):
        orchestrator.process_turn(
            "session-1",
            "invalid",
            create_context_bundle(create_identity()),
        )

    with pytest.raises(
        TypeError,
        match="ContextBundle",
    ):
        orchestrator.process_turn(
            "session-1",
            create_turn(),
            "invalid",
        )