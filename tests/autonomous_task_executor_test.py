from brain.autonomous_task_executor import AutonomousTaskExecutor

executor = AutonomousTaskExecutor()

executor.execute_task(
    "Activate Environment"
)

executor.execute_task(
    "Run Tests"
)

executor.execute_task(
    "Generate Report"
)

executor.show_history()