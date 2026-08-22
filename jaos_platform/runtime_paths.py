"""Canonical runtime-path contracts and resolution for JAOS."""

from __future__ import annotations

import os
import platform
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final


DEFAULT_PROFILE_ID: Final = "default"
RUNTIME_LAYOUT_VERSION: Final = "v1"
RUNTIME_DIRECTORY_ENV: Final = "JAOS_RUNTIME_DIR"

_PROFILE_ID_PATTERN: Final = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_WINDOWS_PLATFORM: Final = "Windows"
_LINUX_PLATFORM: Final = "Linux"
_MACOS_PLATFORM: Final = "Darwin"


class RuntimePathConfigurationError(ValueError):
    """Raised when runtime-path configuration is invalid or unsafe."""


def _validate_profile_id(profile_id: str) -> str:
    if not isinstance(profile_id, str):
        raise RuntimePathConfigurationError(
            "profile_id must be a string matching "
            "^[A-Za-z0-9_-]{1,64}$"
        )

    if _PROFILE_ID_PATTERN.fullmatch(profile_id) is None:
        raise RuntimePathConfigurationError(
            "profile_id must match ^[A-Za-z0-9_-]{1,64}$"
        )

    return profile_id


def _absolute_path(value: os.PathLike[str] | str, name: str) -> Path:
    try:
        path = Path(value)
    except (TypeError, ValueError, OSError) as error:
        raise RuntimePathConfigurationError(
            f"{name} must be a valid absolute path"
        ) from error

    if not path.is_absolute():
        raise RuntimePathConfigurationError(
            f"{name} must be an absolute path"
        )

    return path


def _canonical_path(path: Path, name: str) -> Path:
    try:
        return path.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise RuntimePathConfigurationError(
            f"{name} could not be resolved safely"
        ) from error


@dataclass(frozen=True, slots=True)
class RuntimePaths:
    """Immutable typed paths for one versioned JAOS runtime profile."""

    runtime_root: Path
    profile_id: str = DEFAULT_PROFILE_ID
    version_root: Path = field(init=False)
    profile_root: Path = field(init=False)
    config: Path = field(init=False)
    memory: Path = field(init=False)
    state: Path = field(init=False)
    recovery: Path = field(init=False)
    audit: Path = field(init=False)
    logs: Path = field(init=False)
    exports: Path = field(init=False)
    backups: Path = field(init=False)
    migrations: Path = field(init=False)
    tmp: Path = field(init=False)

    def __post_init__(self) -> None:
        runtime_root = _canonical_path(
            _absolute_path(self.runtime_root, "runtime_root"),
            "runtime_root",
        )
        profile_id = _validate_profile_id(self.profile_id)
        version_root = runtime_root / RUNTIME_LAYOUT_VERSION
        profile_root = version_root / "profiles" / profile_id

        object.__setattr__(self, "runtime_root", runtime_root)
        object.__setattr__(self, "profile_id", profile_id)
        object.__setattr__(self, "version_root", version_root)
        object.__setattr__(self, "profile_root", profile_root)
        object.__setattr__(self, "config", profile_root / "config")
        object.__setattr__(self, "memory", profile_root / "memory")
        object.__setattr__(self, "state", profile_root / "state")
        object.__setattr__(self, "recovery", profile_root / "recovery")
        object.__setattr__(self, "audit", profile_root / "audit")
        object.__setattr__(self, "logs", profile_root / "logs")
        object.__setattr__(self, "exports", profile_root / "exports")
        object.__setattr__(self, "backups", profile_root / "backups")
        object.__setattr__(self, "migrations", profile_root / "migrations")
        object.__setattr__(self, "tmp", profile_root / "tmp")


class RuntimePathResolver:
    """Resolve one safe runtime root without filesystem side effects."""

    def __init__(
        self,
        *,
        environ: Mapping[str, str] | None = None,
        platform_name: str | None = None,
        home_directory: os.PathLike[str] | str | None = None,
    ) -> None:
        self._environ = os.environ if environ is None else environ
        self._platform_name = (
            platform.system()
            if platform_name is None
            else platform_name
        )
        self._home_directory = home_directory

    def resolve(
        self,
        *,
        runtime_root: os.PathLike[str] | str | None = None,
        profile_id: str = DEFAULT_PROFILE_ID,
        repository_root: os.PathLike[str] | str | None = None,
    ) -> RuntimePaths:
        """Resolve paths using explicit, environment, then OS precedence."""

        _validate_profile_id(profile_id)
        selected_root = self._select_runtime_root(runtime_root)
        canonical_root = _canonical_path(selected_root, "runtime_root")

        if repository_root is not None:
            self._validate_repository_containment(
                runtime_root=canonical_root,
                repository_root=repository_root,
            )

        paths = RuntimePaths(
            runtime_root=canonical_root,
            profile_id=profile_id,
        )
        self._validate_profile_layout(paths)
        return paths

    def _select_runtime_root(
        self,
        explicit_root: os.PathLike[str] | str | None,
    ) -> Path:
        if explicit_root is not None:
            return _absolute_path(explicit_root, "runtime_root")

        if RUNTIME_DIRECTORY_ENV in self._environ:
            return _absolute_path(
                self._environ[RUNTIME_DIRECTORY_ENV],
                RUNTIME_DIRECTORY_ENV,
            )

        return self._resolve_os_default()

    def _resolve_os_default(self) -> Path:
        if self._platform_name == _WINDOWS_PLATFORM:
            local_app_data = self._environ.get("LOCALAPPDATA")
            if not local_app_data:
                raise RuntimePathConfigurationError(
                    "LOCALAPPDATA is required for the Windows runtime default"
                )
            return _absolute_path(local_app_data, "LOCALAPPDATA") / "JAOS"

        if self._platform_name == _LINUX_PLATFORM:
            xdg_data_home = self._environ.get("XDG_DATA_HOME")
            if xdg_data_home:
                return _absolute_path(xdg_data_home, "XDG_DATA_HOME") / "jaos"
            return self._resolve_home_directory() / ".local" / "share" / "jaos"

        if self._platform_name == _MACOS_PLATFORM:
            return (
                self._resolve_home_directory()
                / "Library"
                / "Application Support"
                / "JAOS"
            )

        raise RuntimePathConfigurationError(
            f"unsupported operating system for runtime paths: {self._platform_name}"
        )

    def _resolve_home_directory(self) -> Path:
        if self._home_directory is not None:
            return _absolute_path(self._home_directory, "home_directory")

        try:
            home_directory = Path.home()
        except (OSError, RuntimeError) as error:
            raise RuntimePathConfigurationError(
                "the operating-system home directory could not be resolved"
            ) from error

        return _absolute_path(home_directory, "home_directory")

    @staticmethod
    def _validate_profile_layout(paths: RuntimePaths) -> None:
        profiles_root = _canonical_path(
            paths.version_root / "profiles",
            "profiles_root",
        )
        profile_root = _canonical_path(
            paths.profile_root,
            "profile_root",
        )

        try:
            profiles_root.relative_to(paths.runtime_root)
        except ValueError as error:
            raise RuntimePathConfigurationError(
                "the versioned profiles root escapes runtime_root"
            ) from error

        if profile_root != profiles_root / paths.profile_id:
            raise RuntimePathConfigurationError(
                "profile_root escapes its validated profile scope"
            )

        for scope_name in (
            "config",
            "memory",
            "state",
            "recovery",
            "audit",
            "logs",
            "exports",
            "backups",
            "migrations",
            "tmp",
        ):
            scope_path = _canonical_path(
                getattr(paths, scope_name),
                scope_name,
            )
            if scope_path != profile_root / scope_name:
                raise RuntimePathConfigurationError(
                    f"{scope_name} escapes its validated profile scope"
                )

    @staticmethod
    def _validate_repository_containment(
        *,
        runtime_root: Path,
        repository_root: os.PathLike[str] | str,
    ) -> None:
        canonical_repository = _canonical_path(
            _absolute_path(repository_root, "repository_root"),
            "repository_root",
        )

        try:
            runtime_root.relative_to(canonical_repository)
        except ValueError:
            return

        raise RuntimePathConfigurationError(
            "runtime_root must not be the repository root or a descendant of it"
        )


__all__ = [
    "DEFAULT_PROFILE_ID",
    "RUNTIME_DIRECTORY_ENV",
    "RUNTIME_LAYOUT_VERSION",
    "RuntimePathConfigurationError",
    "RuntimePathResolver",
    "RuntimePaths",
]
