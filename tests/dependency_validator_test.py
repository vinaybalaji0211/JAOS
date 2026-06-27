from engineering.dependency_validator import (
    DependencyValidator
)

validator = DependencyValidator()

validator.add_dependency(
    "Workflow Engine",
    "Task Manager"
)

validator.add_dependency(
    "Security Monitor",
    "Audit Logger"
)

validator.validate()