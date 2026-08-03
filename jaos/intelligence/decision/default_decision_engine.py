"""Default Decision Engine for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from jaos.intelligence.decision.confidence_evaluator import (
    ConfidenceEvaluator,
)
from jaos.intelligence.decision.decision_request_validator import (
    DecisionRequestValidator,
)
from jaos.intelligence.decision.decision_strategy_selector import (
    DecisionStrategySelector,
)
from jaos.intelligence.decision.permission_evaluator import (
    PermissionEvaluator,
)
from jaos.intelligence.decision.policy_evaluator import (
    PolicyEvaluator,
)
from jaos.intelligence.interfaces.decision_engine import (
    DecisionEngine,
)
from jaos.intelligence.models.decision_proposal import (
    DecisionProposal,
)
from jaos.intelligence.models.decision_request import (
    DecisionRequest,
)
from jaos.intelligence.models.decision_status import (
    DecisionStatus,
)


class DefaultDecisionEngine(DecisionEngine):
    """
    Default provider-independent implementation of the
    JAOS Decision Engine.
    """

    def __init__(
        self,
        *,
        request_validator: DecisionRequestValidator | None = None,
        strategy_selector: DecisionStrategySelector | None = None,
        policy_evaluator: PolicyEvaluator | None = None,
        permission_evaluator: PermissionEvaluator | None = None,
        confidence_evaluator: ConfidenceEvaluator | None = None,
    ) -> None:
        """Initialize the Decision Engine."""

        self._request_validator = request_validator or DecisionRequestValidator()

        self._strategy_selector = strategy_selector or DecisionStrategySelector()

        self._policy_evaluator = policy_evaluator or PolicyEvaluator()

        self._permission_evaluator = permission_evaluator or PermissionEvaluator()

        self._confidence_evaluator = confidence_evaluator or ConfidenceEvaluator()

        self._ready = False

    @property
    def component_name(self) -> str:
        """Return the stable component name."""

        return "default_decision_engine"

    @property
    def is_ready(self) -> bool:
        """Return whether the engine is ready."""

        return self._ready

    async def initialize(self) -> None:
        """Initialize the Decision Engine."""

        self._ready = True

    async def shutdown(self) -> None:
        """Shutdown the Decision Engine."""

        self._ready = False

    async def make_decision(
        self,
        request: DecisionRequest,
    ) -> DecisionProposal:
        """
        Evaluate a DecisionRequest and produce a
        provider-independent DecisionProposal.
        """

        request = self._request_validator.validate(request)

        strategy = self._strategy_selector.select(request)

        policy_ok = self._policy_evaluator.evaluate(request)

        permission_ok = self._permission_evaluator.evaluate(request)

        approved = policy_ok and permission_ok

        confidence = self._confidence_evaluator.evaluate(request)

        return DecisionProposal(
            request_id=request.request_id,
            identity=request.identity,
            plan_proposal=request.plan_proposal,
            status=(DecisionStatus.APPROVED if approved else DecisionStatus.REJECTED),
            priority=request.priority,
            confidence=confidence,
            approved=approved,
            decision_summary=("Plan approved." if approved else "Plan rejected."),
            decision_rationale=(
                f"Decision evaluated using " f"{strategy.value} strategy."
            ),
        )
