"""
JAOS Component: ResultManager

Purpose:
    Manage execution results inside the Executive Brain.

Responsibilities:
    - Store and retrieve results
    - Query execution history
    - Provide execution statistics
    - Report manager health

Non-Responsibilities:
    - Execute plans
    - Learn from results
    - AI reasoning
    - Memory management
"""

from executive_brain.managers.registry_manager import RegistryManager
from executive_brain.models.result_model import ResultModel


class ResultManager:
    """Manager responsible for managing execution results."""

    def __init__(self, registry_manager: RegistryManager):
        if not isinstance(registry_manager, RegistryManager):
            raise TypeError(
                "registry_manager must be an instance of RegistryManager."
            )

        self.registry_manager = registry_manager
        self.status = "INITIALIZED"

    def initialize(self):
        self.status = "READY"
        return True

    def get_status(self):
        return self.status

    def health_check(self):
        return {
            "result_manager": self.status == "READY",
            "registry_manager": self.registry_manager is not None,
        }

    def add_result(self, result: ResultModel):
        self.registry_manager.result_registry.add_result(result)
        return result

    def get_result(self, result_id: str):
        return self.registry_manager.result_registry.get_result(result_id)

    def list_results(self):
        return self.registry_manager.result_registry.list_results()

    def get_successful_results(self):
        return self.registry_manager.result_registry.get_successful_results()

    def get_failed_results(self):
        return self.registry_manager.result_registry.get_failed_results()

    def get_results_by_execution_plan(self, execution_plan_id: str):
        return self.registry_manager.result_registry.get_by_execution_plan(
            execution_plan_id
        )

    def total_results(self):
        return len(self.list_results())

    def successful_result_count(self):
        return len(self.get_successful_results())

    def failed_result_count(self):
        return len(self.get_failed_results())

    def success_rate(self):
        total = self.total_results()

        if total == 0:
            return 0.0

        return (self.successful_result_count() / total) * 100.0