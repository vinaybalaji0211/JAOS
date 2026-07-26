"""Conversation orchestration for the JAOS Intelligence Platform."""

from __future__ import annotations

from threading import RLock
from typing import Any, cast

from jaos.ai.ai_manager import AIManager
from jaos.ai.ai_models import AIGenerateRequest
from jaos.ai.response.response_models import ParsedResponse
from jaos.intelligence.conversation.conversation_policy import (
    ConversationPolicy,
)
from jaos.intelligence.conversation.conversation_policy_registry import (
    ConversationPolicyRegistry,
)
from jaos.intelligence.conversation.conversation_reference_resolver import (
    ConversationReferenceResolution,
    ConversationReferenceResolver,
)
from jaos.intelligence.conversation.conversation_response_validator import (
    ConversationProviderResponseValidator,
)
from jaos.intelligence.conversation.conversation_session_manager import (
    ConversationSessionManager,
)
from jaos.intelligence.exceptions import (
    IntelligenceConversationError,
    IntelligencePermissionError,
)
from jaos.intelligence.interfaces.conversation_engine import (
    ConversationEngine,
)
from jaos.intelligence.interfaces.prompt_composer import PromptComposer
from jaos.intelligence.models.context_bundle import ContextBundle
from jaos.intelligence.models.conversation_role import ConversationRole
from jaos.intelligence.models.conversation_session import ConversationSession
from jaos.intelligence.models.conversation_turn import ConversationTurn
from jaos.intelligence.models.intelligence_identity import (
    IntelligenceIdentity,
)
from jaos.intelligence.models.intelligence_request import IntelligenceRequest
from jaos.intelligence.models.intelligence_request_type import (
    IntelligenceRequestType,
)
from jaos.intelligence.models.intelligence_result import IntelligenceResult
from jaos.intelligence.models.intelligence_result_status import (
    IntelligenceResultStatus,
)
from jaos.intelligence.prompt.prompt_composition_models import (
    PromptCompositionRequest,
    PromptCompositionResult,
)


class ConversationOrchestrator(ConversationEngine):
    """
    Coordinates one complete JAOS conversation-turn lifecycle.

    The orchestrator owns conversation sequencing but delegates:

    - session mutation to ConversationSessionManager;
    - policy selection to ConversationPolicyRegistry;
    - reference detection to ConversationReferenceResolver;
    - prompt construction to PromptComposer;
    - provider routing and generation to AIManager;
    - provider-response validation to the certified validator.

    It never accesses ProviderManager or provider implementations directly.
    """

    _COMPONENT = "conversation_orchestrator"
    _CLARIFICATION_MESSAGE = (
        "I need clarification before I can safely resolve that reference."
    )

    def __init__(
        self,
        session_manager: ConversationSessionManager,
        policy_registry: ConversationPolicyRegistry,
        reference_resolver: ConversationReferenceResolver,
        prompt_composer: PromptComposer,
        ai_manager: AIManager,
        *,
        template_id: str,
        template_version: str | None = None,
        response_validator: (
            ConversationProviderResponseValidator | None
        ) = None,
    ) -> None:
        if not isinstance(
            session_manager,
            ConversationSessionManager,
        ):
            raise TypeError(
                "session_manager must be a ConversationSessionManager"
            )

        if not isinstance(
            policy_registry,
            ConversationPolicyRegistry,
        ):
            raise TypeError(
                "policy_registry must be a ConversationPolicyRegistry"
            )

        if not isinstance(
            reference_resolver,
            ConversationReferenceResolver,
        ):
            raise TypeError(
                "reference_resolver must be a "
                "ConversationReferenceResolver"
            )

        if not isinstance(prompt_composer, PromptComposer):
            raise TypeError(
                "prompt_composer must implement the PromptComposer contract"
            )

        if not isinstance(ai_manager, AIManager):
            raise TypeError("ai_manager must be an AIManager")

        resolved_validator = (
            response_validator
            or ConversationProviderResponseValidator()
        )

        if not isinstance(
            resolved_validator,
            ConversationProviderResponseValidator,
        ):
            raise TypeError(
                "response_validator must be a "
                "ConversationProviderResponseValidator or None"
            )

        self._session_manager = session_manager
        self._policy_registry = policy_registry
        self._reference_resolver = reference_resolver
        self._prompt_composer = prompt_composer
        self._ai_manager = ai_manager
        self._response_validator = resolved_validator
        self._template_id = self._normalize_template_id(template_id)
        self._template_version = self._normalize_template_version(
            template_version
        )

        self._ready = False
        self._lock = RLock()

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return "conversation-orchestrator"

    @property
    def is_ready(self) -> bool:
        """Return whether the orchestrator can accept work."""

        with self._lock:
            return self._ready

    def initialize(self) -> None:
        """
        Initialize the orchestrator after its prompt dependency is ready.

        Platform composition remains responsible for dependency lifecycle
        ordering. The orchestrator does not initialize shared components.
        """

        if not self._prompt_composer.is_ready:
            raise IntelligenceConversationError(
                "prompt composer must be initialized before the "
                "conversation orchestrator",
                component=self._COMPONENT,
                details={
                    "dependency": self._prompt_composer.component_name,
                    "dependency_ready": False,
                },
            )

        with self._lock:
            self._ready = True

    def shutdown(self) -> None:
        """
        Stop accepting conversation work.

        Shared dependencies are not shut down here because their lifecycle is
        controlled by platform composition.
        """

        with self._lock:
            self._ready = False

    def start_session(
        self,
        identity: IntelligenceIdentity,
        *,
        policy_name: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ConversationSession:
        """Create and return a policy-controlled conversation session."""

        self._require_ready()

        return self._session_manager.start_session(
            identity,
            policy_name=policy_name,
            metadata=metadata,
        )

    def get_session(
        self,
        session_id: str,
    ) -> ConversationSession | None:
        """Return the current immutable session snapshot."""

        self._require_ready()

        return self._session_manager.get_session(session_id)

    def process_turn(
        self,
        session_id: str,
        turn: ConversationTurn,
        context_bundle: ContextBundle,
    ) -> IntelligenceResult:
        """Process one user turn through the approved JAOS boundaries."""

        if not isinstance(turn, ConversationTurn):
            raise TypeError("turn must be a ConversationTurn")

        if not isinstance(context_bundle, ContextBundle):
            raise TypeError(
                "context_bundle must be a ContextBundle"
            )

        self._require_ready(request_id=context_bundle.request_id)

        session = self._session_manager.get_required_session(session_id)
        policy = self._resolve_policy(session)

        self._validate_turn_context(
            session=session,
            turn=turn,
            context_bundle=context_bundle,
            policy=policy,
        )

        reference_resolution = self._reference_resolver.resolve(
            session,
            turn,
            policy,
        )

        updated_session = self._session_manager.append_turn(
            session.session_id,
            turn,
            identity=session.identity,
        )

        if (
            reference_resolution.reference_detected
            and not reference_resolution.resolved
        ):
            return self._build_clarification_result(
                session=updated_session,
                user_turn=turn,
                context_bundle=context_bundle,
                policy=policy,
                reference_resolution=reference_resolution,
            )

        intelligence_request = IntelligenceRequest(
            objective=turn.content,
            request_type=IntelligenceRequestType.CONVERSATION,
            identity=updated_session.identity,
            request_id=context_bundle.request_id,
            session_id=updated_session.session_id,
            context_policy=policy.context_policy,
            permission_constraints=(
                self._collect_permission_constraints(context_bundle)
            ),
            metadata={
                "conversation_turn_id": turn.turn_id,
                "conversation_session_id": updated_session.session_id,
                "conversation_policy": policy.policy_name,
                "context_bundle_id": context_bundle.bundle_id,
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
            },
        )

        try:
            prompt_result = self._prompt_composer.compose(
                PromptCompositionRequest(
                    request=intelligence_request,
                    context_bundle=context_bundle,
                    template_id=self._template_id,
                    template_version=self._template_version,
                    metadata={
                        "conversation_session_id": (
                            updated_session.session_id
                        ),
                        "conversation_turn_id": turn.turn_id,
                        "reference_resolution": (
                            reference_resolution.to_dict()
                        ),
                    },
                )
            )

            provider_response = self._ai_manager.generate_from_request(
                self._build_ai_request(
                    intelligence_request,
                    prompt_result,
                    turn,
                )
            )

            validated_response = self._response_validator.validate(
                provider_response
            )

            if not isinstance(validated_response, ParsedResponse):
                raise IntelligenceConversationError(
                    "AIManager returned an unsupported response type",
                    component=self._COMPONENT,
                    details={
                        "response_type": type(
                            validated_response
                        ).__name__,
                    },
                )

            parsed_response = cast(
                ParsedResponse,
                validated_response,
            )

            self._validate_policy_response_limits(
                parsed_response,
                policy,
            )

            assistant_turn = self._build_provider_assistant_turn(
                session=updated_session,
                response=parsed_response,
                prompt_result=prompt_result,
                reference_resolution=reference_resolution,
                request_id=intelligence_request.request_id,
            )

            final_session = self._session_manager.append_turn(
                updated_session.session_id,
                assistant_turn,
                identity=updated_session.identity,
            )

            return self._build_success_result(
                session=final_session,
                user_turn=turn,
                assistant_turn=assistant_turn,
                response=parsed_response,
                prompt_result=prompt_result,
                policy=policy,
                reference_resolution=reference_resolution,
                request_id=intelligence_request.request_id,
            )

        except Exception as error:
            return self._build_failed_result(
                session=updated_session,
                user_turn=turn,
                context_bundle=context_bundle,
                policy=policy,
                reference_resolution=reference_resolution,
                error=error,
            )

    def close_session(
        self,
        session_id: str,
    ) -> ConversationSession:
        """Close and return a conversation session."""

        self._require_ready()

        return self._session_manager.close_session(session_id)

    def _resolve_policy(
        self,
        session: ConversationSession,
    ) -> ConversationPolicy:
        """Resolve and verify the policy attached to a session."""

        policy_name = session.metadata.get("conversation_policy")

        if (
            policy_name is not None
            and not isinstance(policy_name, str)
        ):
            raise IntelligenceConversationError(
                "conversation session policy metadata is invalid",
                component=self._COMPONENT,
                details={"session_id": session.session_id},
            )

        policy = self._policy_registry.resolve_policy(policy_name)

        if (
            session.context_policy is not None
            and session.context_policy != policy.context_policy
        ):
            raise IntelligenceConversationError(
                "conversation session context policy is inconsistent",
                component=self._COMPONENT,
                details={
                    "session_id": session.session_id,
                    "session_context_policy": (
                        session.context_policy
                    ),
                    "resolved_context_policy": (
                        policy.context_policy
                    ),
                },
            )

        return policy

    def _validate_turn_context(
        self,
        *,
        session: ConversationSession,
        turn: ConversationTurn,
        context_bundle: ContextBundle,
        policy: ConversationPolicy,
    ) -> None:
        """Validate session, turn, identity, and context alignment."""

        if turn.role is not ConversationRole.USER:
            raise IntelligenceConversationError(
                "conversation input turn must use the user role",
                component=self._COMPONENT,
                details={
                    "session_id": session.session_id,
                    "turn_id": turn.turn_id,
                    "actual_role": turn.role.value,
                },
            )

        if turn.session_id != session.session_id:
            raise IntelligenceConversationError(
                "conversation turn session_id does not match session",
                component=self._COMPONENT,
                details={
                    "session_id": session.session_id,
                    "turn_id": turn.turn_id,
                    "turn_session_id": turn.session_id,
                },
            )

        if context_bundle.identity != session.identity:
            raise IntelligencePermissionError(
                "context bundle identity does not match conversation "
                "session identity",
                component=self._COMPONENT,
                details={
                    "session_id": session.session_id,
                    "request_id": context_bundle.request_id,
                },
            )

        if (
            context_bundle.context_policy is not None
            and context_bundle.context_policy
            != policy.context_policy
        ):
            raise IntelligenceConversationError(
                "context bundle policy does not match conversation policy",
                component=self._COMPONENT,
                details={
                    "session_id": session.session_id,
                    "request_id": context_bundle.request_id,
                    "bundle_context_policy": (
                        context_bundle.context_policy
                    ),
                    "conversation_context_policy": (
                        policy.context_policy
                    ),
                },
            )

    @staticmethod
    def _collect_permission_constraints(
        context_bundle: ContextBundle,
    ) -> tuple[str, ...]:
        """Collect unique context permission constraints in stable order."""

        collected: list[str] = []

        for item in context_bundle.items:
            for constraint in item.permission_constraints:
                if constraint not in collected:
                    collected.append(constraint)

        return tuple(collected)

    @staticmethod
    def _build_ai_request(
        intelligence_request: IntelligenceRequest,
        prompt_result: PromptCompositionResult,
        turn: ConversationTurn,
    ) -> AIGenerateRequest:
        """Bridge the compiled Intelligence prompt into AIManager."""

        return AIGenerateRequest(
            prompt=prompt_result.compiled_prompt.text,
            metadata={
                "intelligence_request_id": (
                    intelligence_request.request_id
                ),
                "conversation_session_id": (
                    intelligence_request.session_id
                ),
                "conversation_turn_id": turn.turn_id,
                "prompt_template_reference": (
                    prompt_result.template_reference
                ),
                "prompt_estimated_tokens": (
                    prompt_result.estimated_prompt_tokens
                ),
                "context_item_ids": list(
                    prompt_result.context_item_ids
                ),
                "redacted_item_ids": list(
                    prompt_result.redacted_item_ids
                ),
                "contained_item_ids": list(
                    prompt_result.contained_item_ids
                ),
            },
        )

    @staticmethod
    def _validate_policy_response_limits(
        response: ParsedResponse,
        policy: ConversationPolicy,
    ) -> None:
        """Apply the selected conversation policy to provider output."""

        if len(response.text) > policy.max_provider_response_characters:
            raise IntelligenceConversationError(
                "AI response exceeds the conversation policy "
                "character limit",
                component=ConversationOrchestrator._COMPONENT,
                details={
                    "validation_rule": "policy_response_length",
                    "provider": response.metadata.provider,
                    "model": response.metadata.model,
                    "text_length": len(response.text),
                    "max_characters": (
                        policy.max_provider_response_characters
                    ),
                    "policy_name": policy.policy_name,
                },
            )

        metadata_count = len(response.metadata.source_metadata)

        if metadata_count > policy.max_provider_metadata_items:
            raise IntelligenceConversationError(
                "AI response exceeds the conversation policy "
                "metadata limit",
                component=ConversationOrchestrator._COMPONENT,
                details={
                    "validation_rule": "policy_metadata_count",
                    "provider": response.metadata.provider,
                    "model": response.metadata.model,
                    "metadata_count": metadata_count,
                    "max_metadata_items": (
                        policy.max_provider_metadata_items
                    ),
                    "policy_name": policy.policy_name,
                },
            )

    @staticmethod
    def _build_provider_assistant_turn(
        *,
        session: ConversationSession,
        response: ParsedResponse,
        prompt_result: PromptCompositionResult,
        reference_resolution: ConversationReferenceResolution,
        request_id: str,
    ) -> ConversationTurn:
        """Build the immutable assistant turn from a provider response."""

        return ConversationTurn(
            session_id=session.session_id,
            role=ConversationRole.ASSISTANT,
            content=response.text,
            source="ai_provider",
            context_source_ids=prompt_result.context_item_ids,
            metadata={
                "request_id": request_id,
                "provider_name": response.metadata.provider,
                "provider_model": response.metadata.model,
                "template_reference": (
                    prompt_result.template_reference
                ),
                "prompt_estimated_tokens": (
                    prompt_result.estimated_prompt_tokens
                ),
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
            },
        )

    def _build_clarification_result(
        self,
        *,
        session: ConversationSession,
        user_turn: ConversationTurn,
        context_bundle: ContextBundle,
        policy: ConversationPolicy,
        reference_resolution: ConversationReferenceResolution,
    ) -> IntelligenceResult:
        """Return a deterministic clarification without provider access."""

        assistant_turn = ConversationTurn(
            session_id=session.session_id,
            role=ConversationRole.ASSISTANT,
            content=self._CLARIFICATION_MESSAGE,
            source=self._COMPONENT,
            metadata={
                "request_id": context_bundle.request_id,
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
            },
        )

        final_session = self._session_manager.append_turn(
            session.session_id,
            assistant_turn,
            identity=session.identity,
        )

        return IntelligenceResult(
            request_id=context_bundle.request_id,
            status=(
                IntelligenceResultStatus.REQUIRES_CLARIFICATION
            ),
            output=self._CLARIFICATION_MESSAGE,
            structured_output={
                "session_id": final_session.session_id,
                "user_turn_id": user_turn.turn_id,
                "assistant_turn_id": assistant_turn.turn_id,
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
            },
            metadata={
                "component": self._COMPONENT,
                "conversation_policy": policy.policy_name,
                "provider_invoked": False,
            },
        )

    def _build_success_result(
        self,
        *,
        session: ConversationSession,
        user_turn: ConversationTurn,
        assistant_turn: ConversationTurn,
        response: ParsedResponse,
        prompt_result: PromptCompositionResult,
        policy: ConversationPolicy,
        reference_resolution: ConversationReferenceResolution,
        request_id: str,
    ) -> IntelligenceResult:
        """Build the successful platform-standard intelligence result."""

        return IntelligenceResult(
            request_id=request_id,
            status=IntelligenceResultStatus.SUCCEEDED,
            output=response.text,
            structured_output={
                "session_id": session.session_id,
                "user_turn_id": user_turn.turn_id,
                "assistant_turn_id": assistant_turn.turn_id,
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
                "prompt": {
                    "template_reference": (
                        prompt_result.template_reference
                    ),
                    "estimated_tokens": (
                        prompt_result.estimated_prompt_tokens
                    ),
                    "redacted_item_ids": list(
                        prompt_result.redacted_item_ids
                    ),
                    "contained_item_ids": list(
                        prompt_result.contained_item_ids
                    ),
                },
            },
            context_source_ids=prompt_result.context_item_ids,
            provider_name=response.metadata.provider,
            provider_model=response.metadata.model,
            metadata={
                "component": self._COMPONENT,
                "conversation_policy": policy.policy_name,
                "provider_metadata_item_count": len(
                    response.metadata.source_metadata
                ),
            },
        )

    def _build_failed_result(
        self,
        *,
        session: ConversationSession,
        user_turn: ConversationTurn,
        context_bundle: ContextBundle,
        policy: ConversationPolicy,
        reference_resolution: ConversationReferenceResolution,
        error: Exception,
    ) -> IntelligenceResult:
        """Build a structured failed result without corrupting the session."""

        error_message = str(error).strip()

        if not error_message:
            error_message = "conversation processing failed"

        return IntelligenceResult(
            request_id=context_bundle.request_id,
            status=IntelligenceResultStatus.FAILED,
            structured_output={
                "session_id": session.session_id,
                "user_turn_id": user_turn.turn_id,
                "reference_resolution": (
                    reference_resolution.to_dict()
                ),
            },
            context_source_ids=tuple(
                item.item_id for item in context_bundle.items
            ),
            error_code=type(error).__name__,
            error_message=error_message,
            metadata={
                "component": self._COMPONENT,
                "conversation_policy": policy.policy_name,
                "session_preserved": True,
            },
        )

    def _require_ready(
        self,
        *,
        request_id: str | None = None,
    ) -> None:
        """Reject work while the orchestrator is offline."""

        if self.is_ready:
            return

        details: dict[str, Any] = {"is_ready": False}

        if request_id is not None:
            details["request_id"] = request_id

        raise IntelligenceConversationError(
            "conversation orchestrator is not initialized",
            component=self._COMPONENT,
            details=details,
        )

    @staticmethod
    def _normalize_template_id(template_id: str) -> str:
        """Validate the required prompt-template identifier."""

        if not isinstance(template_id, str):
            raise TypeError("template_id must be a string")

        normalized = template_id.strip()

        if not normalized:
            raise ValueError("template_id must not be empty")

        return normalized

    @staticmethod
    def _normalize_template_version(
        template_version: str | None,
    ) -> str | None:
        """Validate the optional prompt-template version."""

        if template_version is None:
            return None

        if not isinstance(template_version, str):
            raise TypeError(
                "template_version must be a string or None"
            )

        normalized = template_version.strip()

        if not normalized:
            raise ValueError(
                "template_version must not be empty when provided"
            )

        return normalized