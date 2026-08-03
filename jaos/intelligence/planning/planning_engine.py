"""Default Planning Engine implementation for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.interfaces.planning_engine import (
    PlanningEngine,
)
from jaos.intelligence.models.plan_proposal import (
    PlanProposal,
)
from jaos.intelligence.models.planning_request import (
    PlanningRequest,
)
from jaos.intelligence.planning.planning_dependency_resolver import (
    PlanningDependencyResolver,
)
from jaos.intelligence.planning.planning_proposal_validator import (
    PlanningProposalValidator,
)
from jaos.intelligence.planning.planning_request_validator import (
    PlanningRequestValidator,
)
from jaos.intelligence.planning.planning_step_generator import (
    PlanningStepGenerator,
)
from jaos.intelligence.planning.planning_strategy_selector import (
    PlanningStrategySelector,
)


class DefaultPlanningEngine(PlanningEngine):
    """
    Default implementation of the JAOS Planning Engine.

    The Planning Engine is responsible for orchestrating the
    deterministic planning pipeline while delegating all planning
    responsibilities to specialized stateless components.

    Responsibilities
    ----------------
    • Validate planning requests.
    • Select the planning strategy.
    • Generate planning steps.
    • Resolve planning dependencies.
    • Construct validated plan proposals.

    The engine itself contains no planning logic and performs
    no I/O, provider interaction, or persistent state changes.
    """

    def __init__(
        self,
        request_validator: PlanningRequestValidator | None = None,
        strategy_selector: PlanningStrategySelector | None = None,
        step_generator: PlanningStepGenerator | None = None,
        dependency_resolver: PlanningDependencyResolver | None = None,
        proposal_validator: PlanningProposalValidator | None = None,
    ) -> None:
        """Initialize the Planning Engine."""

        self._request_validator = (
            request_validator
            if request_validator is not None
            else PlanningRequestValidator()
        )

        self._strategy_selector = (
            strategy_selector
            if strategy_selector is not None
            else PlanningStrategySelector()
        )

        self._step_generator = (
            step_generator if step_generator is not None else PlanningStepGenerator()
        )

        self._dependency_resolver = (
            dependency_resolver
            if dependency_resolver is not None
            else PlanningDependencyResolver()
        )

        self._proposal_validator = (
            proposal_validator
            if proposal_validator is not None
            else PlanningProposalValidator()
        )

        self._ready = False

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return "planning_engine"

    @property
    def is_ready(self) -> bool:
        """Return whether the engine is ready."""

        return self._ready

    async def initialize(self) -> None:
        """Initialize the Planning Engine."""

        self._ready = True

    async def shutdown(self) -> None:
        """Shutdown the Planning Engine."""

        self._ready = False

    async def create_plan(
        self,
        request: PlanningRequest,
    ) -> PlanProposal:
        """
        Create a deterministic plan proposal.

        This method orchestrates the Planning Engine pipeline while
        delegating all planning responsibilities to specialized
        stateless components.
        """

        validated_request = self._request_validator.validate(
            request,
        )

        strategy = self._strategy_selector.select(
            validated_request,
        )

        generated_steps = self._step_generator.generate(
            validated_request,
            strategy,
        )

        resolved_steps = self._dependency_resolver.resolve(
            generated_steps,
        )

        proposal = self._proposal_validator.validate(
            validated_request,
            resolved_steps,
        )

        return proposal
