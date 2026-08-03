"""Decision request validator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)


class DecisionRequestValidator:
    """
    Validates DecisionRequest instances before they are
    processed by the Decision Engine.

    The validator is intentionally stateless and performs
    structural validation only. Business decisions,
    permission checks, and policy evaluation are handled
    by later stages of the Decision Engine.
    """

    def validate(
        self,
        request: DecisionRequest,
    ) -> DecisionRequest:
        """
        Validate a DecisionRequest.

        Args:
            request:
                The request to validate.

        Returns:
            The validated DecisionRequest.

        Raises:
            TypeError:
                If the supplied object is not a DecisionRequest.

            ValueError:
                If the request contains an invalid PlanProposal.
        """

        if not isinstance(request, DecisionRequest):
            raise TypeError("request must be an instance of DecisionRequest")

        if not request.plan_proposal.steps:
            raise ValueError(
                "decision request must reference a non-empty plan proposal"
            )

        return request
