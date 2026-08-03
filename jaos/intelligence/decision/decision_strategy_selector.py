"""Decision strategy selector for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)
from jaos.intelligence.models.decision_strategy import (
    DecisionStrategy,
)


class DecisionStrategySelector:
    """
    Selects the effective decision strategy for a
    DecisionRequest.

    The selector remains deterministic and stateless.
    Future versions may adapt the strategy based on
    context, policies, or runtime conditions.
    """

    def select(
        self,
        request: DecisionRequest,
    ) -> DecisionStrategy:
        """
        Select the decision strategy.

        Args:
            request:
                The validated decision request.

        Returns:
            The selected DecisionStrategy.
        """

        if not isinstance(request, DecisionRequest):
            raise TypeError("request must be an instance of DecisionRequest")

        return request.decision_strategy
