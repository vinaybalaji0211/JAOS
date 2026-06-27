from infrastructure.storage_intelligence import (
    StorageIntelligence
)

storage = StorageIntelligence()

storage.register_storage(
    "Local Disk",
    "LOCAL",
    "READY"
)

storage.register_storage(
    "Google Drive",
    "CLOUD",
    "READY"
)

storage.register_storage(
    "Vector Store",
    "VECTOR_DB",
    "PENDING"
)

storage.show_storage()

print(
    storage.get_storage(
        "Google Drive"
    )
)