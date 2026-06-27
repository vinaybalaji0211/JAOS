from brain.cloud_memory_connector import (
    CloudMemoryConnector
)

connector = (
    CloudMemoryConnector()
)

connector.status()

connector.connect(
    "Supabase"
)

connector.status()

connector.disconnect()

connector.status()