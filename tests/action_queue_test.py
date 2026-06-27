from core.action_queue import ActionQueue


queue = ActionQueue()

queue.add_action(
    "Load Memory"
)

queue.add_action(
    "Initialize AI Provider"
)

queue.add_action(
    "Check System Health"
)

queue.show_queue()

print()

queue.execute_next()

print()

queue.show_queue()