"""Planning engine contract for the JAOS AI Intelligence Platform."""

from abc import abstractmethod

from jaos.intelligence.interfaces.intelligence_component import (
    IntelligenceComponent,
)
from jaos.intelligence.models.plan_proposal import PlanProposal
from jaos.intelligence.models.planning_request import PlanningRequest


class PlanningEngine(IntelligenceComponent):
    """
    Defines structured plan-proposal generation.

    Implementations decompose approved goals into ordered,
    dependency-aware steps with capabilities, permissions, risks,
    success criteria, and recovery guidance. They must not directly
    invoke tools or execute the generated plan.
    """

    @abstractmethod
    def create_plan(
        self,
        request: PlanningRequest,
    ) -> PlanProposal:
        """Create a non-authoritative plan proposal."""

        raise NotImplementedError