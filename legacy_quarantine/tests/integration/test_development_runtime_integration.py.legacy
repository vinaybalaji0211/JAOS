from development.development_workspace_manager import (
    DevelopmentWorkspaceManager,
)
from jaos_platform.platform_runtime import PlatformRuntime


def test_workspace_manager_registers_with_runtime():
    runtime = PlatformRuntime()

    manager = DevelopmentWorkspaceManager(runtime)

    assert (
        runtime.container.resolve(
            "development_workspace_manager"
        )
        is manager
    )


def test_workspace_manager_updates_runtime_context():
    runtime = PlatformRuntime()

    DevelopmentWorkspaceManager(runtime)

    assert (
        runtime.context.get(
            "development_workspace_manager_status"
        )
        == "READY"
    )


def test_workspace_registration_still_works():
    runtime = PlatformRuntime()

    manager = DevelopmentWorkspaceManager(runtime)

    manager.register_workspace(
        "JAOS",
        "github.com/vinay/jaos",
        "jaos.code-workspace",
    )

    assert manager.workspaces["JAOS"] == {
        "repository": "github.com/vinay/jaos",
        "vscode_workspace": "jaos.code-workspace",
    }