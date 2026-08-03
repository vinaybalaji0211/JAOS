from engineering.configuration_validator import ConfigurationValidator

validator = ConfigurationValidator()

validator.add_required_key(
    "theme"
)

validator.add_required_key(
    "default_ai"
)

validator.set_config(
    "theme",
    "dark"
)

validator.set_config(
    "default_ai",
    "OpenAI"
)

validator.validate()