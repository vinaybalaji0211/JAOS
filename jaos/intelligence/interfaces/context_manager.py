"""Context management contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_bundle import ContextBundle
from jaos.intelligence.models.context_item import ContextItem
from jaos.intelligence.models.intelligence_request import IntelligenceRequest


class IntelligenceContextManager(IntelligenceComponent):
    """
    Defines context assembly and validation operations.

    Implementations may collect candidate context from conversation,
    memory, identity, runtime, capability, and permission sources.
    They must apply trust, relevance, identity, permission, conflict,
    expiry, and token-budget policies before returning a bundle.
    """

    @abstractmethod
    def assemble_context(
        self,
        request: IntelligenceRequest,
        candidate_items: tuple[ContextItem, ...] = (),
    ) -> ContextBundle:
        """Build a validated context bundle for an intelligence request."""

        raise NotImplementedError

    @abstractmethod
    def validate_context(self, bundle: ContextBundle) -> None:
        """Validate that a context bundle satisfies platform policy."""

        raise NotImplementedError