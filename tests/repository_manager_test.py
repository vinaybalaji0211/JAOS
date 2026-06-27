from development.repository_manager import (
    RepositoryManager
)

manager = RepositoryManager()

manager.add_repository(
    "JAOS",
    "C:/JARVIS",
    "https://github.com/vinay/jaos"
)

manager.add_repository(
    "YOLO Project",
    "C:/UNDERWATER OBJECT DETECTION",
    "https://github.com/vinay/yolo",
    "develop"
)

manager.show_repositories()