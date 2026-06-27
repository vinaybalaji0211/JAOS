from brain.event_bus import EventBus


def memory_agent_listener(data):

    print(
        f"Memory Agent received event data: {data}"
    )


def planner_agent_listener(data):

    print(
        f"Planner Agent received event data: {data}"
    )


event_bus = EventBus()

event_bus.subscribe(
    "goal_created",
    memory_agent_listener
)

event_bus.subscribe(
    "goal_created",
    planner_agent_listener
)

event_bus.publish(
    "goal_created",
    {
        "goal": "Build independent 24/7 AI Operating System"
    }
)

event_bus.show_history()