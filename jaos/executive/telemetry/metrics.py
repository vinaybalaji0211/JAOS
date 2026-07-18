from dataclasses import dataclass


@dataclass
class ExecutiveMetrics:
    """
    Runtime metrics for the Executive Platform.
    """

    plans_executed: int = 0
    plans_succeeded: int = 0
    plans_failed: int = 0
    last_plan_steps: int = 0

    def record_success(self, step_count: int) -> None:
        self.plans_executed += 1
        self.plans_succeeded += 1
        self.last_plan_steps = step_count

    def record_failure(self, step_count: int) -> None:
        self.plans_executed += 1
        self.plans_failed += 1
        self.last_plan_steps = step_count

    def success_rate(self) -> float:
        if self.plans_executed == 0:
            return 0.0

        return self.plans_succeeded / self.plans_executed