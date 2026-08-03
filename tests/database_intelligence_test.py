from infrastructure.database_intelligence import DatabaseIntelligence

database = DatabaseIntelligence()

database.register_database(
    "PostgreSQL",
    "RELATIONAL",
    "READY"
)

database.register_database(
    "pgvector",
    "VECTOR",
    "READY"
)

database.register_database(
    "SQLite",
    "LOCAL_CACHE",
    "READY"
)

database.register_database(
    "SecretVault",
    "SECRETS",
    "PENDING"
)

database.show_databases()

print(
    database.get_database(
        "pgvector"
    )
)