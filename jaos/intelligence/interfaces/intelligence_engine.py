"""Primary engine contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.intelligence_request import IntelligenceRequest
from jaos.intelligence.models.intelligence_result import IntelligenceResult


class IntelligenceEngine(IntelligenceComponent):
    """
    Defines the primary request-processing boundary.

    Implementations coordinate context, conversation, reasoning,
    planning, agent orchestration, provider-backed AI generation, and
    execution-proposal construction while preserving platform boundaries.
    """

    @abstractmethod
    def process_request(
        self,
        request: IntelligenceRequest,
    ) -> IntelligenceResult:
        """Process an intelligence request and return a structured result."""

        raise NotImplementedError