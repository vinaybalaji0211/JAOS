from kernel.kernel_event_bus import KernelEventBus

bus = KernelEventBus()

bus.publish_event(
    "Security Platform",
    "PERMISSION_GRANTED",
    "Vinay can open VS Code."
)

bus.publish_event(
    "Workflow Platform",
    "TASK_STARTED",
    "Morning Briefing started."
)

bus.show_events()