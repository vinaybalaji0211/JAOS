from brain.screen_workflow_recorder import ScreenWorkflowRecorder

recorder = ScreenWorkflowRecorder()

recorder.start_recording(
    "VS Code Project Workflow"
)

recorder.record_step(
    "VS Code Project Workflow",
    "Open VS Code"
)

recorder.record_step(
    "VS Code Project Workflow",
    "Open Project Folder"
)

recorder.record_step(
    "VS Code Project Workflow",
    "Activate Environment"
)

recorder.record_step(
    "VS Code Project Workflow",
    "Run Tests"
)

recorder.show_workflow(
    "VS Code Project Workflow"
)