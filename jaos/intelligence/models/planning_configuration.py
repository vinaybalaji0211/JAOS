"""Planning configuration model for the JAOS AI Intelligence Platform."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from jaos.intelligence.models.fallback_policy import FallbackPolicy
from jaos.intelligence.models.optimization_goal import (
    OptimizationGoal,
)
from jaos.intelligence.models.parallel_execution_policy import (
    ParallelExecutionPolicy,
)
from jaos.intelligence.models.planning_strategy import (
    PlanningStrategy,
)


@dataclass(frozen=True, slots=True)
class PlanningConfiguration:
    """
    Immutable planning configuration for the Planning Engine.

    This value object defines how planning should be performed.
    It contains operational planning policies only and never
    contains cognitive understanding, execution state, or
    provider-specific information.
    """

    strategy: PlanningStrategy = PlanningStrategy.DIRECT

    parallel_policy: ParallelExecutionPolicy = ParallelExecutionPolicy.AUTO

    fallback_policy: FallbackPolicy = FallbackPolicy.REACTIVE

    optimization_goal: OptimizationGoal = OptimizationGoal.BALANCED

    max_depth: int = 5

    time_budget_ms: int | None = 5000

    simulation_mode: bool = False

    def __post_init__(self) -> None:
        """Validate planning configuration invariants."""

        if not isinstance(
            self.strategy,
            PlanningStrategy,
        ):
            raise TypeError("strategy must be a PlanningStrategy")

        if not isinstance(
            self.parallel_policy,
            ParallelExecutionPolicy,
        ):
            raise TypeError("parallel_policy must be a ParallelExecutionPolicy")

        if not isinstance(
            self.fallback_policy,
            FallbackPolicy,
        ):
            raise TypeError("fallback_policy must be a FallbackPolicy")

        if not isinstance(
            self.optimization_goal,
            OptimizationGoal,
        ):
            raise TypeError("optimization_goal must be an OptimizationGoal")

        if isinstance(
            self.max_depth,
            bool,
        ) or not isinstance(
            self.max_depth,
            int,
        ):
            raise TypeError("max_depth must be an integer")

        if self.max_depth <= 0:
            raise ValueError("max_depth must be greater than zero")

        if self.time_budget_ms is not None:

            if isinstance(
                self.time_budget_ms,
                bool,
            ) or not isinstance(
                self.time_budget_ms,
                int,
            ):
                raise TypeError("time_budget_ms must be an integer or None")

            if self.time_budget_ms < 100:
                raise ValueError("time_budget_ms must be at least 100 milliseconds")

        if not isinstance(
            self.simulation_mode,
            bool,
        ):
            raise TypeError("simulation_mode must be a boolean")

    def to_dict(self) -> dict[str, Any]:
        """Return a provider-independent dictionary representation."""

        return {
            "strategy": self.strategy.value,
            "parallel_policy": self.parallel_policy.value,
            "fallback_policy": self.fallback_policy.value,
            "optimization_goal": self.optimization_goal.value,
            "max_depth": self.max_depth,
            "time_budget_ms": self.time_budget_ms,
            "simulation_mode": self.simulation_mode,
        }
