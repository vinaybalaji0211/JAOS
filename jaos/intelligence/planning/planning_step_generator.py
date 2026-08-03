"""Planning step generator for the JAOS AI Intelligence Platform."""

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
from jaos.intelligence.models.proposed_plan_step import (
    ProposedPlanStep,
)


class PlanningStepGenerator:
    """
    Generates deterministic planning steps.

    This component is responsible solely for transforming a
    validated PlanningRequest and PlanningStrategy into one or
    more immutable ProposedPlanStep objects.

    Responsibilities
    ----------------
    • Operate deterministically.
    • Remain completely stateless.
    • Never modify the PlanningRequest.
    • Never perform I/O.
    • Never execute planning.
    • Never maintain internal state.

    Version 1 produces a single deterministic planning step.
    Future implementations may generate hierarchical or adaptive
    execution plans while preserving this public interface.
    """

    def generate(
        self,
        request: PlanningRequest,
        strategy: PlanningStrategy,
    ) -> tuple[ProposedPlanStep, ...]:
        """
        Generate planning steps.

        Args:
            request:
                A validated PlanningRequest.

            strategy:
                The selected planning strategy.

        Returns:
            An immutable tuple of ProposedPlanStep objects.

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
                    "generator": "PlanningStepGenerator",
                    "expected_type": "PlanningRequest",
                    "received_type": type(request).__name__,
                },
            )

        if not isinstance(
            strategy,
            PlanningStrategy,
        ):
            raise IntelligenceValidationError(
                "PlanningStrategy is required.",
                request_id=request.request_id,
                details={
                    "generator": "PlanningStepGenerator",
                    "expected_type": "PlanningStrategy",
                    "received_type": type(strategy).__name__,
                },
            )

        return (self._create_step(request),)

    def _create_step(
        self,
        request: PlanningRequest,
    ) -> ProposedPlanStep:
        """
        Create the initial planning step.
        """

        return ProposedPlanStep(
            description=request.goal,
            step_order=1,
            required_capability=self._determine_required_capability(
                request,
            ),
            expected_output=request.goal,
            success_condition=self._determine_success_condition(
                request,
            ),
        )

    def _determine_required_capability(
        self,
        request: PlanningRequest,
    ) -> str:
        """
        Determine the capability required by the planning step.

        Future implementations may inspect planning policies,
        metadata, reasoning results, or strategy selection.

        Version 1 always returns the planning capability.
        """

        return "planning"

    def _determine_success_condition(
        self,
        request: PlanningRequest,
    ) -> str:
        """
        Determine the success condition for the planning step.

        Future implementations may derive richer success criteria.

        Version 1 uses the first declared success criterion when
        available and otherwise falls back to a deterministic
        default.
        """

        if request.success_criteria:
            return request.success_criteria[0]

        return "Planning step completed."
