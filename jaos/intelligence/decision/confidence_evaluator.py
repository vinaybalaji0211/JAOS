"""Confidence evaluator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.models.decision_confidence import (
    DecisionConfidence,
)
from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)


class ConfidenceEvaluator:
    """
    Evaluates the confidence level associated with a
    DecisionRequest.

    The evaluator is intentionally stateless. Future
    implementations may incorporate historical execution
    outcomes, model certainty, plan complexity, risk
    analysis, and runtime context.
    """

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> DecisionConfidence:
        """
        Evaluate the confidence of a decision request.

        Args:
            request:
                The validated decision request.

        Returns:
            The assessed DecisionConfidence.
        """

        if not isinstance(request, DecisionRequest):
            raise TypeError("request must be an instance of DecisionRequest")

        # Phase 8 default implementation.
        return DecisionConfidence.HIGH
