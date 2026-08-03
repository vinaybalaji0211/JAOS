from infrastructure.multi_provider_task_composer import MultiProviderTaskComposer

composer = MultiProviderTaskComposer()

composer.add_step(
    "Planner Agent",
    "Break task into subtasks"
)

composer.add_step(
    "OpenAI",
    "Generate frontend architecture"
)

composer.add_step(
    "Local LLM",
    "Generate boilerplate code"
)

composer.add_step(
    "GitHub",
    "Create repository"
)

composer.add_step(
    "Testing Agent",
    "Run automated tests"
)

composer.show_plan()