"""Planning request validator for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.exceptions import (
    IntelligenceValidationError,
)
from jaos.intelligence.models.planning_request import (
    PlanningRequest,
)


class PlanningRequestValidator:
    """
    Validates PlanningRequest pipeline invariants.

    This validator operates exclusively at the Planning Engine
    pipeline boundary.

    Responsibilities
    ----------------
    • Validate pipeline-level invariants.
    • Ensure the request is suitable to enter planning.
    • Never modify the request.
    • Never normalize request data.
    • Never perform planning.
    • Never perform I/O.
    • Never maintain state.

    The underlying PlanningRequest model is responsible for all
    structural validation. This validator only verifies that the
    request satisfies Planning Engine requirements.
    """

    def validate(
        self,
        request: PlanningRequest,
    ) -> PlanningRequest:
        """
        Validate a PlanningRequest for the Planning Engine pipeline.

        Args:
            request:
                Immutable planning request.

        Returns:
            The same immutable PlanningRequest.

        Raises:
            IntelligenceValidationError:
                If the request cannot enter the Planning Engine.
        """

        self._validate_request_type(request)
        self._validate_reasoning_result(request)
        self._validate_configuration(request)
        self._validate_goal(request)

        return request

    # ---------------------------------------------------------
    # Internal Validation Helpers
    # ---------------------------------------------------------

    def _validate_request_type(
        self,
        request: PlanningRequest,
    ) -> None:
        """
        Ensure the supplied object is a PlanningRequest.
        """

        if not isinstance(
            request,
            PlanningRequest,
        ):
            raise IntelligenceValidationError(
                "PlanningRequest is required.",
                details={
                    "validator": ("PlanningRequestValidator"),
                    "expected_type": ("PlanningRequest"),
                    "received_type": (type(request).__name__),
                },
            )

    def _validate_reasoning_result(
        self,
        request: PlanningRequest,
    ) -> None:
        """
        Ensure a validated ReasoningResult is available.
        """

        if request.reasoning_result is None:
            raise IntelligenceValidationError(
                "PlanningRequest must contain a ReasoningResult.",
                request_id=request.request_id,
                details={
                    "validator": ("PlanningRequestValidator"),
                    "field": "reasoning_result",
                },
            )

    def _validate_configuration(
        self,
        request: PlanningRequest,
    ) -> None:
        """
        Ensure planning configuration is available.
        """

        if request.configuration is None:
            raise IntelligenceValidationError(
                "PlanningRequest must contain a PlanningConfiguration.",
                request_id=request.request_id,
                details={
                    "validator": ("PlanningRequestValidator"),
                    "field": "configuration",
                },
            )

    def _validate_goal(
        self,
        request: PlanningRequest,
    ) -> None:
        """
        Ensure the planning objective is available.

        The PlanningRequest model already guarantees that the goal
        is a normalized non-empty string. This check certifies that
        the Planning Engine has a usable planning objective.
        """

        if not request.goal:
            raise IntelligenceValidationError(
                "PlanningRequest must contain a planning goal.",
                request_id=request.request_id,
                details={
                    "validator": ("PlanningRequestValidator"),
                    "field": "goal",
                },
            )

        if not request.goal.strip():
            raise IntelligenceValidationError(
                "PlanningRequest planning goal cannot be blank.",
                request_id=request.request_id,
                details={
                    "validator": ("PlanningRequestValidator"),
                    "field": "goal",
                },
            )
