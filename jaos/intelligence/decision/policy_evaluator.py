"""Policy evaluator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)


class PolicyEvaluator:
    """
    Evaluates whether a DecisionRequest satisfies
    applicable platform policies.

    The evaluator is intentionally stateless.
    Future implementations may consult configurable
    policy engines, organizational rules, or security
    frameworks.
    """

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> bool:
        """
        Evaluate platform policies.

        Args:
            request:
                The validated decision request.

        Returns:
            True if the request satisfies current
            platform policies.
        """

        if not isinstance(request, DecisionRequest):
            raise TypeError("request must be an instance of DecisionRequest")

        # Phase 8 default implementation:
        # All validated requests satisfy policy.
        return True
