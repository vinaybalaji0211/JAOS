from executive_brain.models.result_model import ResultModel

result = ResultModel(
    success=True,
    message="VS Code launched successfully.",
    related_execution_plan_id="PLAN-001"
)

result.add_metadata(
    "execution_time_ms",
    842
)

print()
print(result.to_dict())