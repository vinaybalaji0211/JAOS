from brain.distributed_memory_system import (
    DistributedMemorySystem
)

memory = (
    DistributedMemorySystem()
)

memory.add_node(
    "PrimaryCloud"
)

memory.add_node(
    "BackupCloud"
)

memory.store(
    "PrimaryCloud",
    "Knowledge Graph"
)

memory.store(
    "BackupCloud",
    "Evolution Memory"
)

memory.show_nodes()