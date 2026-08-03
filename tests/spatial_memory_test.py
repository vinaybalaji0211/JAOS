from brain.spatial_memory import SpatialMemory

memory = SpatialMemory()

memory.remember_location(
    "Logs",
    "C:\\JARVIS\\logs",
    "folder"
)

memory.remember_location(
    "Provider Config",
    "C:\\JARVIS\\config\\providers.json",
    "file"
)

memory.remember_location(
    "Exports",
    "C:\\JARVIS\\exports",
    "folder"
)

memory.remember_location(
    "Brain Modules",
    "C:\\JARVIS\\brain",
    "folder"
)

memory.show_locations()