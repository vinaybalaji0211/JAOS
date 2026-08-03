"""Permission evaluator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)


class PermissionEvaluator:
    """
    Evaluates whether a DecisionRequest satisfies
    the permissions required for execution.

    The evaluator is intentionally stateless.
    Future implementations may integrate with the
    JAOS Security Platform and permission framework.
    """

    def evaluate(
        self,
        request: DecisionRequest,
    ) -> bool:
        """
        Evaluate execution permissions.

        Args:
            request:
                The validated decision request.

        Returns:
            True if all required permissions are
            satisfied.
        """

        if not isinstance(request, DecisionRequest):
            raise TypeError("request must be an instance of DecisionRequest")

        # Phase 8 default implementation:
        # Permission evaluation is deferred until
        # the Security Platform is implemented.
        return True
