from engineering.package_registry import PackageRegistry

registry = PackageRegistry()

registry.register_package(
    "ultralytics",
    "8.4.37"
)

registry.register_package(
    "torch",
    "2.5.1+cu121"
)

registry.show_packages()