"""Planning dependency resolver for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.exceptions import (
    IntelligenceValidationError,
)
from jaos.intelligence.models.proposed_plan_step import (
    ProposedPlanStep,
)


class PlanningDependencyResolver:
    """
    Validates and certifies planning-step dependencies.

    This component is responsible solely for verifying that a
    collection of ProposedPlanStep instances forms a valid
    dependency graph suitable for proposal construction.

    Responsibilities
    ----------------
    • Operate deterministically.
    • Remain completely stateless.
    • Never modify planning steps.
    • Never reorder planning steps.
    • Never perform I/O.
    • Never execute planning.

    Version 1 performs defensive validation only and returns the
    original immutable tuple unchanged.

    Future versions may perform dependency optimization,
    topological sorting, cycle detection, and parallelization
    analysis while preserving the public API.
    """

    def resolve(
        self,
        steps: tuple[ProposedPlanStep, ...],
    ) -> tuple[ProposedPlanStep, ...]:
        """
        Validate planning-step dependencies.

        Args:
            steps:
                Immutable planning steps.

        Returns:
            The same immutable tuple of planning steps.

        Raises:
            IntelligenceValidationError:
                If the dependency graph is invalid.
        """

        self._validate_steps(steps)
        self._validate_unique_step_ids(steps)
        self._validate_dependencies(steps)

        return steps

    def _validate_steps(
        self,
        steps: tuple[ProposedPlanStep, ...],
    ) -> None:
        """Validate the supplied planning-step collection."""

        if not isinstance(
            steps,
            tuple,
        ):
            raise IntelligenceValidationError(
                "Planning steps must be provided as a tuple.",
                details={
                    "resolver": "PlanningDependencyResolver",
                    "expected_type": "tuple",
                    "received_type": type(steps).__name__,
                },
            )

        if not steps:
            raise IntelligenceValidationError(
                "Planning step collection must not be empty.",
                details={
                    "resolver": "PlanningDependencyResolver",
                },
            )

        for step in steps:
            if not isinstance(
                step,
                ProposedPlanStep,
            ):
                raise IntelligenceValidationError(
                    "Planning steps must contain only ProposedPlanStep instances.",
                    details={
                        "resolver": "PlanningDependencyResolver",
                        "received_type": type(step).__name__,
                    },
                )

    def _validate_unique_step_ids(
        self,
        steps: tuple[ProposedPlanStep, ...],
    ) -> None:
        """Ensure every planning step has a unique identifier."""

        step_ids = tuple(step.step_id for step in steps)

        if len(step_ids) != len(set(step_ids)):
            raise IntelligenceValidationError(
                "Planning step identifiers must be unique.",
                details={
                    "resolver": "PlanningDependencyResolver",
                },
            )

    def _validate_dependencies(
        self,
        steps: tuple[ProposedPlanStep, ...],
    ) -> None:
        """Validate dependency references."""

        known_steps = {step.step_id for step in steps}

        for step in steps:
            if step.step_id in step.dependencies:
                raise IntelligenceValidationError(
                    "A planning step cannot depend on itself.",
                    details={
                        "resolver": "PlanningDependencyResolver",
                        "step_id": step.step_id,
                    },
                )

            for dependency in step.dependencies:
                if dependency not in known_steps:
                    raise IntelligenceValidationError(
                        "Planning step dependency references an unknown step.",
                        details={
                            "resolver": "PlanningDependencyResolver",
                            "step_id": step.step_id,
                            "dependency": dependency,
                        },
                    )
