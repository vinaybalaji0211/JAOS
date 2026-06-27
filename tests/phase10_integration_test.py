from brain.scheduler import Scheduler
from brain.background_task_manager import (
    BackgroundTaskManager
)
from brain.event_system import EventSystem
from brain.goal_scheduler import GoalScheduler
from brain.autonomous_task_executor import (
    AutonomousTaskExecutor
)
from brain.goal_stack import GoalStack


print("\n=== PHASE 10 INTEGRATION TEST ===\n")

# Scheduler
scheduler = Scheduler()

scheduler.add_task(
    "Run diagnostics",
    "08:00"
)

scheduler.show_tasks()

# Background Tasks
background = BackgroundTaskManager()

background.add_task(
    "Memory Consolidation"
)

background.show_tasks()

# Events
events = EventSystem()

events.emit(
    "TASK_COMPLETED",
    {
        "task": "Run diagnostics"
    }
)

events.show_events()

# Goal Scheduler
goal_scheduler = GoalScheduler()

goal_scheduler.schedule_goal(
    "Build JARVIS OS",
    "weekly",
    priority=1
)

goal_scheduler.show_goals()

# Goal Stack
stack = GoalStack()

stack.add_goal(
    "Build JARVIS OS",
    1
)

stack.add_goal(
    "Run health checks",
    2
)

stack.show_goals()

# Autonomous Executor
AutonomousTaskExecutor.show_execution(

    task="Run diagnostics",

    strategy="SEQUENTIAL",

    safety_decision="ALLOW",

    confidence=95,

    required_tools_available=True

)

print("\n=== PHASE 10 COMPLETE ===")