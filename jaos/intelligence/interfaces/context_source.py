"""Context source contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_item import (
    ContextItem,
)
from jaos.intelligence.models.intelligence_request import (
    IntelligenceRequest,
)


class IntelligenceContextSource(IntelligenceComponent):
    """
    Defines the provider-independent contract for intelligence context
    sources.

    A Context Source is responsible exclusively for collecting
    candidate contextual information from a single logical source and
    translating it into ContextItem domain models.

    Implementations may adapt sources such as:

    - Memory Platform
    - Conversation history
    - Identity services
    - Runtime state
    - Capability registries
    - Permission services
    - Other approved intelligence context providers

    The Context Source represents the context acquisition boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Collect context from exactly one logical source
    - Produce immutable ContextItem collections
    - Remain free of observable side effects

    Implementations shall not:

    - Perform reasoning
    - Assemble context bundles
    - Generate execution plans
    - Construct provider-specific prompts
    - Perform provider routing
    - Execute tools
    - Execute external actions
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """
        Return the stable context source name.

        The returned value uniquely identifies the context source within
        the JAOS Intelligence Platform.
        """

        raise NotImplementedError

    @abstractmethod
    async def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        """
        Collect candidate context items.

        Implementations retrieve contextual information from their
        underlying source and translate it into provider-independent
        ContextItem domain models.

        Args:
            request:
                The intelligence request requiring contextual
                information.

        Returns:
            A tuple of candidate ContextItem instances.
        """

        raise NotImplementedError
