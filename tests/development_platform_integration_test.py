from development.build_test_manager import BuildTestManager
from development.development_workspace_manager import DevelopmentWorkspaceManager
from development.git_manager import GitManager
from development.github_manager import GitHubManager
from development.repository_manager import RepositoryManager
from development.vscode_manager import VSCodeManager

print("\n===== DEVELOPMENT PLATFORM TEST =====\n")

git = GitManager()
git.register_repository(
    "JAOS",
    "C:/JARVIS",
    "main"
)

github = GitHubManager()
github.register_repository(
    "JAOS",
    "https://github.com/vinay/jaos"
)

repo = RepositoryManager()
repo.add_repository(
    "JAOS",
    "C:/JARVIS",
    "https://github.com/vinay/jaos"
)

vscode = VSCodeManager()
vscode.register_workspace(
    "JAOS Workspace",
    "JAOS"
)

workspace = DevelopmentWorkspaceManager()
workspace.register_workspace(
    "JAOS Development",
    "JAOS",
    "JAOS Workspace"
)

build = BuildTestManager()
build.register_project(
    "JAOS",
    "python main.py",
    "python -m pytest"
)

print("\n===== COMPONENT STATUS =====\n")

git.show_repositories()
github.show_repositories()
repo.show_repositories()
vscode.show_workspaces()
workspace.show_workspaces()
build.show_projects()

print("\n===== DEVELOPMENT PLATFORM COMPLETE =====")