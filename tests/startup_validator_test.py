from engineering.startup_validator import StartupValidator

validator = StartupValidator()

validator.add_required_service(
    "JAOS Core"
)

validator.add_required_service(
    "Memory Manager"
)

validator.add_required_service(
    "Security Manager"
)

validator.register_service(
    "JAOS Core",
    True
)

validator.register_service(
    "Memory Manager",
    True
)

validator.register_service(
    "Security Manager",
    True
)

validator.validate()