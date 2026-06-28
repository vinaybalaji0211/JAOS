from executive_brain.common.enums import LifecycleStatus
from executive_brain.models.result_model import ResultModel
from executive_brain.registries.base_registry import BaseRegistry


class ResultRegistry(BaseRegistry):
    """
    Registry responsible for storing and managing ResultModel objects.

    Responsibilities:
    - Store results
    - Retrieve results
    - Update results
    - Remove results
    - Filter results

    Non-Responsibilities:
    - Execute plans
    - Analyze results
    - Learn from results
    - Retry execution
    """

    def __init__(self):
        super().__init__()

    def add_result(self, result: ResultModel):
        if not isinstance(result, ResultModel):
            raise TypeError("result must be an instance of ResultModel.")

        self.add(result.result_id, result)

    def get_result(self, result_id: str):
        return self.get(result_id)

    def update_result(self, result: ResultModel):
        if not isinstance(result, ResultModel):
            raise TypeError("result must be an instance of ResultModel.")

        self.update(result.result_id, result)

    def remove_result(self, result_id: str):
        return self.remove(result_id)

    def list_results(self):
        return self.list_all()

    def get_by_status(self, status: LifecycleStatus):
        return [
            result
            for result in self.list_all()
            if result.status == status
        ]

    def get_by_execution_plan(self, execution_plan_id: str):
        return [
            result
            for result in self.list_all()
            if result.related_execution_plan_id == execution_plan_id
        ]

    def get_successful_results(self):
        return [
            result
            for result in self.list_all()
            if result.success is True
        ]

    def get_failed_results(self):
        return [
            result
            for result in self.list_all()
            if result.success is False
        ]

    def get_completed_results(self):
        return self.get_by_status(LifecycleStatus.COMPLETED)

    def get_incomplete_results(self):
        return [
            result
            for result in self.list_all()
            if result.status != LifecycleStatus.COMPLETED
        ]