from development.github_manager import GitHubManager

github = GitHubManager()

github.register_repository(
    "JAOS",
    "https://github.com/vinay/jaos"
)

github.register_repository(
    "YOLO Project",
    "https://github.com/vinay/yolo",
    "DISCONNECTED"
)

github.show_repositories()