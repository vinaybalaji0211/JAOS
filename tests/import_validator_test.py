from engineering.import_validator import ImportValidator

validator = ImportValidator()

validator.add_import("security.permission_manager")
validator.add_import("dashboard.mission_control")
validator.add_import("system_services.backup_manager")
validator.add_import("knowledge.knowledge_graph")

validator.validate()