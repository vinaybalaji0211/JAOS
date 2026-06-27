from workflow.task_queue import TaskQueue

queue = TaskQueue()

queue.add_task(
    "Read Emails",
    "LOW"
)

queue.add_task(
    "Deploy Website",
    "HIGH"
)

queue.add_task(
    "Generate Notes",
    "MEDIUM"
)

queue.show_queue()

print("\nNext Task:")

print(
    queue.next_task()
)