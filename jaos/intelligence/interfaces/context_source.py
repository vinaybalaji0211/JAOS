"""Context source contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.context_item import ContextItem
from jaos.intelligence.models.intelligence_request import IntelligenceRequest


class IntelligenceContextSource(IntelligenceComponent):
    """
    Defines a provider-independent source of intelligence context.

    Implementations may adapt the Memory Platform, conversation history,
    identity services, runtime state, capability registries, permission
    services, or other approved sources into ContextItem contracts.
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Return the stable context-source name."""

        raise NotImplementedError

    @abstractmethod
    def collect_context(
        self,
        request: IntelligenceRequest,
    ) -> tuple[ContextItem, ...]:
        """Collect candidate context items for a request."""

        raise NotImplementedError