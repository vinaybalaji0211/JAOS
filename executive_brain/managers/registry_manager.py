from executive_brain.registries.intent_registry import IntentRegistry
from executive_brain.registries.decision_registry import DecisionRegistry
from executive_brain.registries.goal_registry import GoalRegistry
from executive_brain.registries.mission_registry import MissionRegistry
from executive_brain.registries.execution_plan_registry import ExecutionPlanRegistry
from executive_brain.registries.result_registry import ResultRegistry


class RegistryManager:
    """
    Central manager responsible for coordinating JAOS registry instances.

    Responsibilities:
    - Own registry instances
    - Provide centralized registry access
    - Provide registry health information
    - Support registry lookup by name

    Non-Responsibilities:
    - Store model data directly
    - Execute plans
    - Make decisions
    - Perform AI reasoning
    """

    def __init__(self):
        self.intent_registry = IntentRegistry()
        self.decision_registry = DecisionRegistry()
        self.goal_registry = GoalRegistry()
        self.mission_registry = MissionRegistry()
        self.execution_plan_registry = ExecutionPlanRegistry()
        self.result_registry = ResultRegistry()

        self._registry_map = {
            "intent": self.intent_registry,
            "decision": self.decision_registry,
            "goal": self.goal_registry,
            "mission": self.mission_registry,
            "execution_plan": self.execution_plan_registry,
            "result": self.result_registry,
        }

    def list_registries(self):
        return list(self._registry_map.keys())

    def get_registry(self, registry_name: str):
        if registry_name not in self._registry_map:
            raise KeyError(
                f"Unknown registry '{registry_name}'. "
                f"Available registries: {self.list_registries()}"
            )

        return self._registry_map[registry_name]

    def health_check(self):
        return {
            registry_name: registry is not None
            for registry_name, registry in self._registry_map.items()
        }

    def registry_counts(self):
        return {
            registry_name: registry.count()
            for registry_name, registry in self._registry_map.items()
        }