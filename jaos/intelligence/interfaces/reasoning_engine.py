"""Reasoning engine contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.reasoning_request import ReasoningRequest
from jaos.intelligence.models.reasoning_result import ReasoningResult


class ReasoningEngine(IntelligenceComponent):
    """
    Defines structured reasoning operations.

    Implementations interpret objectives, identify assumptions,
    alternatives, missing information, risks, clarifications, and
    approvals. Results expose concise reasoning summaries rather than
    private model chain-of-thought.
    """

    @abstractmethod
    def reason(
        self,
        request: ReasoningRequest,
    ) -> ReasoningResult:
        """Perform structured reasoning for a validated request."""

        raise NotImplementedError