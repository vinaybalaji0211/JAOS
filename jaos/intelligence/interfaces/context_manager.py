"""Context management contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_bundle import (
    ContextBundle,
)
from jaos.intelligence.models.context_item import (
    ContextItem,
)
from jaos.intelligence.models.intelligence_request import (
    IntelligenceRequest,
)


class IntelligenceContextManager(IntelligenceComponent):
    """
    Defines the provider-independent contract for context management.

    The Intelligence Context Manager is responsible exclusively for
    assembling, validating, and synthesizing contextual information for
    intelligence processing.

    Implementations perform context management activities such as:

    - Context collection
    - Context normalization
    - Context validation
    - Relevance filtering
    - Trust evaluation
    - Permission filtering
    - Conflict resolution
    - Token-budget optimization
    - Context bundle synthesis

    The Intelligence Context Manager represents the contextual
    information boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Produce validated ContextBundle instances
    - Preserve identity isolation
    - Remain free of observable side effects

    Implementations shall not:

    - Execute tools
    - Perform reasoning
    - Generate execution plans
    - Enforce execution policies
    - Construct provider-specific prompts
    - Perform provider routing
    - Execute external actions
    """

    @abstractmethod
    async def assemble_context(
        self,
        request: IntelligenceRequest,
        candidate_items: tuple[ContextItem, ...] = (),
    ) -> ContextBundle:
        """
        Assemble a validated context bundle.

        Implementations collect, evaluate, normalize, and validate
        contextual information before producing a provider-independent
        ContextBundle.

        Args:
            request:
                The intelligence request requiring contextual support.
            candidate_items:
                Optional candidate context items supplied by callers.

        Returns:
            A validated ContextBundle.
        """

        raise NotImplementedError

    @abstractmethod
    async def validate_context(
        self,
        bundle: ContextBundle,
    ) -> None:
        """
        Validate a context bundle against platform policies.

        Args:
            bundle:
                The ContextBundle to validate.

        Raises:
            ContextValidationException:
                If the supplied bundle violates platform rules.
        """

        raise NotImplementedError
