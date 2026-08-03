from brain.secrets_manager import SecretsManager

manager = SecretsManager()

manager.store(
    "OPENAI_API_KEY",
    "secret_value_1"
)

manager.store(
    "GEMINI_API_KEY",
    "secret_value_2"
)

manager.show_keys()

print()

print(
    manager.retrieve(
        "OPENAI_API_KEY"
    )
)