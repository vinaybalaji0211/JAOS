from workflow.dependency_manager import (
    DependencyManager
)

manager = DependencyManager()

manager.add_dependency(
    "Deploy Website",
    "Run Tests"
)

manager.add_dependency(
    "Run Tests",
    "Generate Code"
)

manager.add_dependency(
    "Generate Code",
    "Research"
)

manager.show_dependencies()

print(
    manager.get_dependencies(
        "Deploy Website"
    )
)