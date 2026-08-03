"""Planning proposal validator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.exceptions import (
    IntelligenceValidationError,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)
from jaos.intelligence.models.planning_request import (
    PlanningRequest,
)
from jaos.intelligence.models.proposal_status import (
    ProposalStatus,
)
from jaos.intelligence.models.proposed_plan_step import (
    ProposedPlanStep,
)


class PlanningProposalValidator:
    """
    Constructs and validates immutable plan proposals.

    Responsibilities
    ----------------
    • Construct a provider-independent PlanProposal.
    • Validate Planning Engine output.
    • Never modify PlanningRequest.
    • Never modify ProposedPlanStep objects.
    • Never perform planning.
    • Never perform I/O.
    • Remain completely stateless.

    This component is the only Planning Engine component
    responsible for constructing PlanProposal instances.
    """

    def validate(
        self,
        request: PlanningRequest,
        steps: tuple[ProposedPlanStep, ...],
    ) -> PlanProposal:
        """
        Construct a validated plan proposal.

        Args:
            request:
                Validated planning request.

            steps:
                Validated planning steps.

        Returns:
            Immutable PlanProposal.

        Raises:
            IntelligenceValidationError:
                If the supplied arguments are invalid.
        """

        if not isinstance(
            request,
            PlanningRequest,
        ):
            raise IntelligenceValidationError(
                "PlanningRequest is required.",
                details={
                    "validator": "PlanningProposalValidator",
                    "expected_type": "PlanningRequest",
                    "received_type": type(request).__name__,
                },
            )

        if not isinstance(
            steps,
            tuple,
        ):
            raise IntelligenceValidationError(
                "Planning steps must be a tuple.",
                request_id=request.request_id,
                details={
                    "validator": "PlanningProposalValidator",
                    "expected_type": "tuple",
                    "received_type": type(steps).__name__,
                },
            )

        if not steps:
            raise IntelligenceValidationError(
                "Planning proposal must contain at least one step.",
                request_id=request.request_id,
                details={
                    "validator": "PlanningProposalValidator",
                },
            )

        return PlanProposal(
            planning_id=request.planning_id,
            request_id=request.request_id,
            goal=request.goal,
            identity=request.identity,
            steps=steps,
            expected_outcomes=self._build_expected_outcomes(
                request,
            ),
            success_criteria=self._build_success_criteria(
                request,
            ),
            reasoning_result_id=(request.reasoning_result.request_id),
            status=ProposalStatus.DRAFT,
            confidence=1.0,
        )

    def _build_expected_outcomes(
        self,
        request: PlanningRequest,
    ) -> tuple[str, ...]:
        """
        Build proposal expected outcomes.

        Future implementations may derive richer outcomes
        from reasoning, planning policies, or strategy.
        """

        return (f"Complete objective: {request.goal}",)

    def _build_success_criteria(
        self,
        request: PlanningRequest,
    ) -> tuple[str, ...]:
        """
        Build proposal success criteria.

        Future implementations may synthesize richer
        success conditions.
        """

        if request.success_criteria:
            return request.success_criteria

        return ("Planning objective completed.",)
