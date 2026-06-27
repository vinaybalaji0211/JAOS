from brain.context_manager import ContextManager


context = ContextManager()

context.update_context(
    "current_goal",
    "Build Iron-Man-level JARVIS"
)

context.update_context(
    "current_task",
    "Executive Brain"
)

context.update_context(
    "current_user_request",
    "Continue roadmap"
)

context.update_context(
    "current_agent",
    "Master Brain Agent"
)

context.update_context(
    "current_mode",
    "EXECUTIVE"
)

context.add_recent_context(
    "Completed Decision Engine"
)

context.add_recent_context(
    "Completed Cognitive Load Manager"
)

context.show_context()