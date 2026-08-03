"""Planning strategy selector for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.exceptions import (
    IntelligenceValidationError,
)
from jaos.intelligence.models.planning_request import (
    PlanningRequest,
)
from jaos.intelligence.models.planning_strategy import (
    PlanningStrategy,
)


class PlanningStrategySelector:
    """
    Selects the planning strategy for the Planning Engine.

    This component is responsible solely for determining which
    planning strategy should be used for a validated planning
    request.

    Responsibilities
    ----------------
    • Operate deterministically.
    • Remain completely stateless.
    • Never modify the PlanningRequest.
    • Never perform I/O.
    • Never execute planning.
    • Never maintain internal state.

    Version 1 simply returns the strategy specified by the
    validated PlanningConfiguration. Future versions may select
    strategies dynamically while preserving this public API.
    """

    def select(
        self,
        request: PlanningRequest,
    ) -> PlanningStrategy:
        """
        Select the planning strategy.

        Args:
            request:
                A validated PlanningRequest.

        Returns:
            The planning strategy to use.

        Raises:
            IntelligenceValidationError:
                If the supplied request is invalid.
        """

        if not isinstance(
            request,
            PlanningRequest,
        ):
            raise IntelligenceValidationError(
                "PlanningRequest is required.",
                details={
                    "selector": "PlanningStrategySelector",
                    "expected_type": "PlanningRequest",
                    "received_type": type(request).__name__,
                },
            )

        strategy = request.configuration.strategy

        if not isinstance(
            strategy,
            PlanningStrategy,
        ):
            raise IntelligenceValidationError(
                "PlanningRequest contains an invalid planning strategy.",
                request_id=request.request_id,
                details={
                    "selector": "PlanningStrategySelector",
                    "field": "configuration.strategy",
                    "received_type": type(strategy).__name__,
                },
            )

        return strategy
