from __future__ import annotations

import inspect
import os
import subprocess
import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import jaos_platform.runtime_paths as runtime_paths_module
from jaos_platform.runtime_paths import (
    DEFAULT_PROFILE_ID,
    RuntimePathConfigurationError,
    RuntimePathResolver,
    RuntimePaths,
)


def create_resolver(
    *,
    environ: dict[str, str] | None = None,
    platform_name: str = "Linux",
    home_directory: Path | None = None,
) -> RuntimePathResolver:
    return RuntimePathResolver(
        environ={} if environ is None else environ,
        platform_name=platform_name,
        home_directory=home_directory,
    )


def test_runtime_paths_is_immutable(tmp_path: Path) -> None:
    paths = RuntimePaths(tmp_path / "runtime")

    with pytest.raises(FrozenInstanceError):
        paths.runtime_root = tmp_path / "other"  # type: ignore[misc]


def test_runtime_paths_derives_versioned_profile_layout(
    tmp_path: Path,
) -> None:
    runtime_root = tmp_path / "runtime"

    paths = RuntimePaths(runtime_root, profile_id="profile_1")

    version_root = runtime_root / "v1"
    profile_root = version_root / "profiles" / "profile_1"

    assert paths.runtime_root == runtime_root
    assert paths.version_root == version_root
    assert paths.profile_root == profile_root
    assert paths.config == profile_root / "config"
    assert paths.memory == profile_root / "memory"
    assert paths.state == profile_root / "state"
    assert paths.recovery == profile_root / "recovery"
    assert paths.audit == profile_root / "audit"
    assert paths.logs == profile_root / "logs"
    assert paths.exports == profile_root / "exports"
    assert paths.backups == profile_root / "backups"
    assert paths.migrations == profile_root / "migrations"
    assert paths.tmp == profile_root / "tmp"


def test_default_profile_is_default(tmp_path: Path) -> None:
    paths = RuntimePaths(tmp_path / "runtime")

    assert DEFAULT_PROFILE_ID == "default"
    assert paths.profile_id == "default"
    assert paths.profile_root.name == "default"


@pytest.mark.parametrize(
    "profile_id",
    (
        "A",
        "profile-1",
        "PROFILE_2",
        "a" * 64,
    ),
)
def test_valid_custom_profile_ids_are_accepted(
    tmp_path: Path,
    profile_id: str,
) -> None:
    paths = RuntimePaths(tmp_path / "runtime", profile_id=profile_id)

    assert paths.profile_id == profile_id
    assert paths.profile_root.name == profile_id


@pytest.mark.parametrize(
    "profile_id",
    (
        "",
        ".",
        "..",
        "a" * 65,
        "with space",
        " leading",
        "trailing ",
        "profile/name",
        "profile\\name",
        "/absolute",
        "C:\\runtime",
        "\\\\server\\share",
        "profile.name",
        "profile@name",
        "prøfile",
    ),
)
def test_invalid_profile_ids_are_rejected(
    tmp_path: Path,
    profile_id: str,
) -> None:
    with pytest.raises(RuntimePathConfigurationError):
        RuntimePaths(tmp_path / "runtime", profile_id=profile_id)


def test_non_string_profile_id_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimePathConfigurationError):
        RuntimePaths(
            tmp_path / "runtime",
            profile_id=123,  # type: ignore[arg-type]
        )


def test_explicit_runtime_root_has_highest_precedence(
    tmp_path: Path,
) -> None:
    explicit_root = tmp_path / "explicit"
    resolver = create_resolver(
        environ={"JAOS_RUNTIME_DIR": "relative-environment-root"},
        platform_name="Unsupported",
    )

    paths = resolver.resolve(runtime_root=explicit_root)

    assert paths.runtime_root == explicit_root


def test_environment_runtime_root_precedes_os_default(
    tmp_path: Path,
) -> None:
    environment_root = tmp_path / "environment"
    resolver = create_resolver(
        environ={"JAOS_RUNTIME_DIR": str(environment_root)},
        platform_name="Unsupported",
    )

    paths = resolver.resolve()

    assert paths.runtime_root == environment_root


def test_relative_environment_runtime_root_is_rejected() -> None:
    resolver = create_resolver(
        environ={"JAOS_RUNTIME_DIR": "relative-runtime"},
    )

    with pytest.raises(
        RuntimePathConfigurationError,
        match="JAOS_RUNTIME_DIR must be an absolute path",
    ):
        resolver.resolve()


def test_relative_explicit_runtime_root_is_rejected() -> None:
    resolver = create_resolver()

    with pytest.raises(
        RuntimePathConfigurationError,
        match="runtime_root must be an absolute path",
    ):
        resolver.resolve(runtime_root="relative-runtime")


def test_windows_default_uses_local_app_data(tmp_path: Path) -> None:
    local_app_data = tmp_path / "local-app-data"
    resolver = create_resolver(
        environ={"LOCALAPPDATA": str(local_app_data)},
        platform_name="Windows",
    )

    paths = resolver.resolve()

    assert paths.runtime_root == local_app_data / "JAOS"


def test_windows_default_requires_local_app_data() -> None:
    resolver = create_resolver(platform_name="Windows")

    with pytest.raises(
        RuntimePathConfigurationError,
        match="LOCALAPPDATA is required",
    ):
        resolver.resolve()


def test_linux_default_uses_xdg_data_home(tmp_path: Path) -> None:
    xdg_data_home = tmp_path / "xdg-data"
    resolver = create_resolver(
        environ={"XDG_DATA_HOME": str(xdg_data_home)},
        platform_name="Linux",
        home_directory=tmp_path / "unused-home",
    )

    paths = resolver.resolve()

    assert paths.runtime_root == xdg_data_home / "jaos"


def test_linux_default_falls_back_to_home(tmp_path: Path) -> None:
    home_directory = tmp_path / "home"
    resolver = create_resolver(
        platform_name="Linux",
        home_directory=home_directory,
    )

    paths = resolver.resolve()

    assert paths.runtime_root == home_directory / ".local" / "share" / "jaos"


def test_macos_default_uses_application_support(tmp_path: Path) -> None:
    home_directory = tmp_path / "home"
    resolver = create_resolver(
        platform_name="Darwin",
        home_directory=home_directory,
    )

    paths = resolver.resolve()

    assert paths.runtime_root == (
        home_directory / "Library" / "Application Support" / "JAOS"
    )


def test_unsupported_os_default_is_rejected() -> None:
    resolver = create_resolver(platform_name="Unsupported")

    with pytest.raises(
        RuntimePathConfigurationError,
        match="unsupported operating system",
    ):
        resolver.resolve()


def test_runtime_root_equal_to_repository_root_is_rejected(
    tmp_path: Path,
) -> None:
    repository_root = tmp_path / "repository"
    repository_root.mkdir()
    resolver = create_resolver()

    with pytest.raises(
        RuntimePathConfigurationError,
        match="must not be the repository root",
    ):
        resolver.resolve(
            runtime_root=repository_root,
            repository_root=repository_root,
        )


def test_runtime_root_inside_repository_root_is_rejected(
    tmp_path: Path,
) -> None:
    repository_root = tmp_path / "repository"
    repository_root.mkdir()
    resolver = create_resolver()

    with pytest.raises(
        RuntimePathConfigurationError,
        match="must not be the repository root",
    ):
        resolver.resolve(
            runtime_root=repository_root / "runtime",
            repository_root=repository_root,
        )


def test_canonical_traversal_inside_repository_is_rejected(
    tmp_path: Path,
) -> None:
    repository_root = tmp_path / "repository"
    repository_root.mkdir()
    traversal_root = repository_root / "nested" / ".." / "runtime"
    resolver = create_resolver()

    with pytest.raises(RuntimePathConfigurationError):
        resolver.resolve(
            runtime_root=traversal_root,
            repository_root=repository_root,
        )


def test_profile_symlink_escape_is_rejected(tmp_path: Path) -> None:
    runtime_root = tmp_path / "runtime"
    profiles_root = runtime_root / "v1" / "profiles"
    outside_profile = tmp_path / "outside-profile"
    profiles_root.mkdir(parents=True)
    outside_profile.mkdir()

    try:
        (profiles_root / "default").symlink_to(
            outside_profile,
            target_is_directory=True,
        )
    except OSError as error:
        pytest.skip(f"directory symlinks are unavailable: {error}")

    resolver = create_resolver()

    with pytest.raises(
        RuntimePathConfigurationError,
        match="profile_root escapes",
    ):
        resolver.resolve(runtime_root=runtime_root)


def _create_directory_junction(link_path: Path, target_path: Path) -> None:
    """Create a Windows directory junction without requiring elevation.

    A junction is a Windows-specific reparse point and is distinct from a
    directory symlink: creating one needs no privilege, which is why this
    check can execute where the symlink check cannot. ``mklink`` is a
    ``cmd`` builtin, so ``cmd.exe`` is invoked explicitly with an argument
    list rather than through a shell.
    """

    completed = subprocess.run(
        [
            "cmd",
            "/c",
            "mklink",
            "/J",
            str(link_path),
            str(target_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        raise OSError(
            f"mklink /J exited {completed.returncode}: {detail}"
        )


def _remove_directory_junction(link_path: Path) -> None:
    """Remove only the junction, never the directory it points at.

    ``os.rmdir`` unlinks the reparse point itself. ``shutil.rmtree`` must
    never be used here: it does not treat a junction as a link on Windows
    and would recurse into and destroy the external target's contents.
    """

    os.rmdir(link_path)


@pytest.mark.skipif(
    sys.platform != "win32",
    reason="directory junctions are a Windows-specific reparse point",
)
def test_profile_junction_escape_is_rejected(tmp_path: Path) -> None:
    """A profile reached through a junction must fail canonical containment."""

    runtime_root = tmp_path / "runtime"
    profiles_root = runtime_root / "v1" / "profiles"
    outside_profile = tmp_path / "outside-junction-target"
    profiles_root.mkdir(parents=True)
    outside_profile.mkdir()

    junction_path = profiles_root / DEFAULT_PROFILE_ID

    try:
        _create_directory_junction(junction_path, outside_profile)
    except OSError as error:
        pytest.skip(f"directory junctions are unavailable: {error}")

    try:
        assert junction_path.exists()

        canonical_target = junction_path.resolve()
        canonical_profiles_root = profiles_root.resolve()

        assert canonical_target == outside_profile.resolve()
        assert canonical_target != (
            canonical_profiles_root / DEFAULT_PROFILE_ID
        )
        with pytest.raises(ValueError):
            canonical_target.relative_to(canonical_profiles_root)

        resolver = create_resolver()

        with pytest.raises(
            RuntimePathConfigurationError,
            match="profile_root escapes",
        ):
            resolver.resolve(runtime_root=runtime_root)

        assert list(outside_profile.iterdir()) == []
    finally:
        _remove_directory_junction(junction_path)

    assert not junction_path.exists()
    assert outside_profile.is_dir()
    assert list(outside_profile.iterdir()) == []


def test_runtime_root_outside_repository_root_is_accepted(
    tmp_path: Path,
) -> None:
    repository_root = tmp_path / "repository"
    repository_root.mkdir()
    runtime_root = tmp_path / "runtime"
    resolver = create_resolver()

    paths = resolver.resolve(
        runtime_root=runtime_root,
        repository_root=repository_root,
    )

    assert paths.runtime_root == runtime_root


def test_relative_repository_root_is_rejected(tmp_path: Path) -> None:
    resolver = create_resolver()

    with pytest.raises(
        RuntimePathConfigurationError,
        match="repository_root must be an absolute path",
    ):
        resolver.resolve(
            runtime_root=tmp_path / "runtime",
            repository_root="relative-repository",
        )


def test_resolution_creates_no_files_or_directories(
    tmp_path: Path,
) -> None:
    runtime_root = tmp_path / "not-created"
    before = tuple(tmp_path.iterdir())
    resolver = create_resolver()

    paths = resolver.resolve(runtime_root=runtime_root)

    assert paths.runtime_root == runtime_root
    assert tuple(tmp_path.iterdir()) == before
    assert not runtime_root.exists()


def test_resolution_does_not_mutate_environment(tmp_path: Path) -> None:
    environment = {
        "JAOS_RUNTIME_DIR": str(tmp_path / "runtime"),
        "SENTINEL": "unchanged",
    }
    before = environment.copy()
    resolver = create_resolver(environ=environment)

    resolver.resolve()

    assert environment == before


def test_implementation_has_no_repository_specific_path_or_cwd_lookup() -> None:
    source = inspect.getsource(runtime_paths_module)
    repository_specific_path = "C:" + "\\JARVIS"

    assert repository_specific_path not in source
    assert "Path.cwd(" not in source
    assert "os.getcwd(" not in source
    assert "git" not in source.lower()
