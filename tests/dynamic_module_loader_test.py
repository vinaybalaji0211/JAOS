from brain.dynamic_module_loader import (
    DynamicModuleLoader
)

loader = DynamicModuleLoader()

loader.load(
    "Weather Plugin"
)

loader.load(
    "Browser Plugin"
)

loader.show_modules()

loader.unload(
    "Weather Plugin"
)

loader.reload(
    "Weather Plugin"
)

loader.show_modules()