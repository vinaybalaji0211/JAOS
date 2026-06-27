from brain.task_priority_manager import (
    TaskPriorityManager
)


tasks = [
    {
        "task": "Run safety check",
        "urgency": 5,
        "importance": 5,
        "safety": 5,
        "goal_relevance": 4
    },
    {
        "task": "Clean temporary memory",
        "urgency": 2,
        "importance": 3,
        "safety": 5,
        "goal_relevance": 2
    },
    {
        "task": "Plan next development phase",
        "urgency": 3,
        "importance": 5,
        "safety": 5,
        "goal_relevance": 5
    }
]

TaskPriorityManager.show_ranked_tasks(
    tasks
)