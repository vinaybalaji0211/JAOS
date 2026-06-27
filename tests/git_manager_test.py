from development.git_manager import GitManager

git = GitManager()

git.register_repository(
    "JAOS",
    "C:/JARVIS",
    "main"
)

git.register_repository(
    "YOLO Project",
    "C:/UNDERWATER OBJECT DETECTION",
    "develop"
)

git.show_repositories()