from engineering.platform_registry import PlatformRegistry

registry = PlatformRegistry()

registry.register_platform(
    "Security Platform",
    "v1 Alpha",
    "ACTIVE",
    True
)

registry.register_platform(
    "Engineering & Validation",
    "v1 Alpha",
    "IN DEVELOPMENT",
    False
)

registry.show_platforms()