"""Decision engine contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.decision_proposal import (
    DecisionProposal,
)
from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)


class DecisionEngine(IntelligenceComponent):
    """
    Provider-independent contract for JAOS Decision Engines.

    A Decision Engine evaluates a validated DecisionRequest
    and produces a DecisionProposal.
    """

    @abstractmethod
    async def make_decision(
        self,
        request: DecisionRequest,
    ) -> DecisionProposal:
        """
        Evaluate a DecisionRequest and produce
        a DecisionProposal.
        """

        raise NotImplementedError
