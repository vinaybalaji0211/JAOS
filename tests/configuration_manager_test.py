from system_services.configuration_manager import (
    ConfigurationManager
)

config = ConfigurationManager()

config.set_value(
    "theme",
    "dark"
)

config.set_value(
    "default_ai",
    "OpenAI"
)

config.show_config()

print()

print(
    "Theme:",
    config.get_value("theme")
)