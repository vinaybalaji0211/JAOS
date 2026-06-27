from brain.task_execution_planner import (
    TaskExecutionPlanner
)

planner = TaskExecutionPlanner()

planner.create_plan(
    "Train YOLO Model",
    [
        "Activate environment",
        "Verify dataset",
        "Load model",
        "Train model",
        "Validate model",
        "Generate report"
    ]
)

planner.show_plan(
    "Train YOLO Model"
)