from brain.background_executive_observer import BackgroundExecutiveObserver

observer = BackgroundExecutiveObserver()

observer.update_observation(
    "current_goals",
    [
        "Build strong JARVIS",
        "Prepare 24/7 operation"
    ]
)

observer.update_observation(
    "pending_tasks",
    [
        "Maintenance Scheduler",
        "Memory Consolidation"
    ]
)

observer.update_observation(
    "system_status",
    "OK"
)

observer.update_observation(
    "security_status",
    "OK"
)

observer.update_observation(
    "plugin_status",
    "OK"
)

observer.update_observation(
    "recent_failures",
    []
)

observer.show_observations()