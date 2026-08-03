from brain.event_system import EventSystem

events = EventSystem()

events.emit(
    "TASK_COMPLETED",
    {
        "task": "Health check"
    }
)

events.emit(
    "LOW_MEMORY",
    {
        "available_ram": "700MB"
    }
)

events.emit(
    "PROVIDER_FAILED",
    {
        "provider": "OpenAI"
    }
)

events.show_events()