from kernel.runtime_context import RuntimeContext

context = RuntimeContext()

context.update_context(
    "current_user",
    "Vinay"
)

context.update_context(
    "active_project",
    "JAOS"
)

context.update_context(
    "active_ai_provider",
    "OpenAI"
)

context.show_context()