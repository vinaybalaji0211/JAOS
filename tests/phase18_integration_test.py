from brain.embodied_intelligence_core import EmbodiedIntelligenceCore
from brain.application_skill_learner import ApplicationSkillLearner
from brain.screen_workflow_recorder import ScreenWorkflowRecorder
from brain.task_execution_planner import TaskExecutionPlanner
from brain.autonomous_task_executor import AutonomousTaskExecutor
from brain.environment_understanding_engine import (
    EnvironmentUnderstandingEngine
)
from brain.skill_library import SkillLibrary
from brain.embodied_learning_engine import (
    EmbodiedLearningEngine
)

print("\n=== PHASE 18 INTEGRATION TEST ===\n")

core = EmbodiedIntelligenceCore()
core.set_environment("Windows Desktop")
core.register_skill("Application Control")
core.show_status()

learner = ApplicationSkillLearner()
learner.learn_application(
    "VS Code",
    "Run Python projects"
)
learner.show_applications()

recorder = ScreenWorkflowRecorder()
recorder.start_recording(
    "VS Code Workflow"
)
recorder.record_step(
    "VS Code Workflow",
    "Open VS Code"
)
recorder.record_step(
    "VS Code Workflow",
    "Run Tests"
)
recorder.show_workflow(
    "VS Code Workflow"
)

planner = TaskExecutionPlanner()
planner.create_plan(
    "Run Project",
    [
        "Open Project",
        "Activate Environment",
        "Run Tests"
    ]
)
planner.show_plan(
    "Run Project"
)

executor = AutonomousTaskExecutor()
executor.execute_task(
    "Activate Environment"
)
executor.execute_task(
    "Run Tests"
)
executor.show_history()

env = EnvironmentUnderstandingEngine()
env.update_environment(
    "OS",
    "Windows 11"
)
env.update_environment(
    "Project",
    "JARVIS"
)
env.show_environment()

library = SkillLibrary()
library.add_skill(
    "YOLO Training",
    "Train and validate YOLO models"
)
library.show_skills()

learning = EmbodiedLearningEngine()
learning.learn(
    "Workflow",
    "Environment should be activated before tests."
)
learning.show_learning()

print("\n=== PHASE 18 COMPLETE ===")