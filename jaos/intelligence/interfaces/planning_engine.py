"""Planning engine contract for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)
from jaos.intelligence.models.planning_request import (
    PlanningRequest,
)


class PlanningEngine(IntelligenceComponent):
    """
    Defines the provider-independent contract for strategic planning.

    The Planning Engine is responsible exclusively for transforming a
    validated PlanningRequest into a structured PlanProposal.

    Implementations perform strategic planning activities such as:

    - Strategy construction
    - Dependency analysis
    - Planning graph (DAG) generation
    - Execution ordering
    - Parallelization opportunity identification
    - Resource estimation
    - Fallback strategy generation
    - Plan proposal synthesis

    The Planning Engine represents the strategic planning boundary.

    Implementations shall:

    - Operate asynchronously
    - Use JAOS domain models exclusively
    - Remain provider independent
    - Produce deterministic plan proposals
    - Remain free of observable side effects

    Implementations shall not:

    - Execute tools
    - Perform policy evaluation
    - Enforce permissions
    - Modify persistent memory
    - Construct provider-specific prompts
    - Perform provider routing
    - Execute external actions
    """

    @abstractmethod
    async def create_plan(
        self,
        request: PlanningRequest,
    ) -> PlanProposal:
        """
        Create a structured plan proposal.

        The implementation transforms a validated PlanningRequest into
        a provider-independent PlanProposal representing the strategic
        execution graph for the requested objective.

        This operation represents the single public entry point into the
        planning process. All subordinate planning activities remain
        encapsulated as implementation details.

        Args:
            request:
                The validated planning request.

        Returns:
            A structured provider-independent PlanProposal.

        Raises:
            PlanningException:
                If a valid plan proposal cannot be produced.
        """

        raise NotImplementedError
