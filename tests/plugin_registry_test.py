from brain.plugin_registry import PluginRegistry

registry = PluginRegistry()

registry.register_plugin(
    name="Weather Plugin",
    version="1.0",
    author="Vinay",
    capabilities=[
        "weather_lookup"
    ],
    dependencies=[
        "requests"
    ],
    permissions=[
        "web_access"
    ],
    trust_score=80
)

registry.register_plugin(
    name="Browser Plugin",
    version="1.0",
    author="Vinay",
    capabilities=[
        "web_browsing"
    ],
    dependencies=[],
    permissions=[
        "web_access",
        "read_screen"
    ],
    trust_score=70
)

registry.update_status(
    "Weather Plugin",
    "ACTIVE"
)

registry.show_plugins()