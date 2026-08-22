from __future__ import annotations

import hashlib
import os
from collections.abc import Callable, Iterator
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path

import pytest

from jaos_platform.runtime_paths import (
    RUNTIME_DIRECTORY_ENV,
    RuntimePathResolver,
    RuntimePaths,
)


_REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
_PROTECTED_REPOSITORY_AREAS = ("data", "config", "logs", "exports")
_TEST_PROFILE_ID = "pytest"

TestRuntimePathsFactory = Callable[[Path], RuntimePaths]
RepositoryWriteGuardFactory = Callable[
    [Path | None],
    AbstractContextManager[None],
]
RuntimeEnvironmentFactory = Callable[
    [],
    AbstractContextManager[RuntimePaths],
]


def _resolve_test_runtime_paths(base_path: Path) -> RuntimePaths:
    if not base_path.is_absolute():
        raise ValueError("the test runtime base path must be absolute")

    return RuntimePathResolver(
        environ={},
        platform_name="Test",
    ).resolve(
        runtime_root=base_path / "jaos-runtime",
        profile_id=_TEST_PROFILE_ID,
        repository_root=_REPOSITORY_ROOT,
    )


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _snapshot_protected_state(repository_root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}

    def record(path: Path) -> None:
        relative_path = path.relative_to(repository_root).as_posix()
        try:
            if path.is_symlink():
                snapshot[relative_path] = f"symlink:{os.readlink(path)}"
                return
            if path.is_file():
                snapshot[relative_path] = f"file:{_file_digest(path)}"
                return
            if path.is_dir():
                snapshot[relative_path] = "directory"
                for child in sorted(path.iterdir(), key=lambda item: item.name):
                    record(child)
                return
            snapshot[relative_path] = "other"
        except OSError as error:
            raise AssertionError(
                f"unable to fingerprint protected path: {relative_path}"
            ) from error

    for area_name in _PROTECTED_REPOSITORY_AREAS:
        area_path = repository_root / area_name
        if area_path.exists() or area_path.is_symlink():
            record(area_path)

    return snapshot


def _protected_state_changes(
    before: dict[str, str],
    after: dict[str, str],
) -> list[str]:
    changes: list[str] = []
    for relative_path in sorted(before.keys() | after.keys()):
        if relative_path not in before:
            changes.append(f"created: {relative_path}")
        elif relative_path not in after:
            changes.append(f"deleted: {relative_path}")
        elif before[relative_path] != after[relative_path]:
            changes.append(f"modified: {relative_path}")
    return changes


@contextmanager
def _guard_repository_state(
    repository_root: Path,
) -> Iterator[None]:
    if not repository_root.is_absolute():
        raise ValueError("repository_root must be absolute")

    canonical_root = repository_root.resolve(strict=False)
    if not canonical_root.is_dir():
        raise ValueError("repository_root must identify an existing directory")

    before = _snapshot_protected_state(canonical_root)
    try:
        yield
    finally:
        after = _snapshot_protected_state(canonical_root)
        changes = _protected_state_changes(before, after)
        if changes:
            details = "\n".join(f"- {change}" for change in changes)
            raise AssertionError(
                "protected repository runtime state changed:\n" + details
            )


@contextmanager
def _scoped_runtime_environment(
    runtime_paths: RuntimePaths,
) -> Iterator[RuntimePaths]:
    with pytest.MonkeyPatch.context() as scoped_environment:
        scoped_environment.setenv(
            RUNTIME_DIRECTORY_ENV,
            str(runtime_paths.runtime_root),
        )
        yield runtime_paths


@pytest.fixture(scope="function")
def jaos_runtime_paths_factory() -> TestRuntimePathsFactory:
    """Build canonical RuntimePaths below a caller-owned temporary path."""

    return _resolve_test_runtime_paths


@pytest.fixture(scope="function")
def jaos_runtime_paths(
    tmp_path: Path,
    jaos_runtime_paths_factory: TestRuntimePathsFactory,
) -> RuntimePaths:
    """Provide isolated canonical paths rooted at tmp_path/jaos-runtime."""

    return jaos_runtime_paths_factory(tmp_path)


@pytest.fixture(scope="function")
def jaos_runtime_environment_context(
    jaos_runtime_paths: RuntimePaths,
) -> RuntimeEnvironmentFactory:
    """Provide a context for subprocess-compatible runtime resolution."""

    return lambda: _scoped_runtime_environment(jaos_runtime_paths)


@pytest.fixture(scope="function")
def jaos_runtime_environment(
    jaos_runtime_environment_context: RuntimeEnvironmentFactory,
) -> Iterator[RuntimePaths]:
    """Temporarily expose the isolated root through JAOS_RUNTIME_DIR."""

    with jaos_runtime_environment_context() as runtime_paths:
        yield runtime_paths


@pytest.fixture(scope="function")
def repository_write_guard() -> RepositoryWriteGuardFactory:
    """Return an opt-in guard for protected repository runtime state."""

    def create_guard(
        repository_root: Path | None = None,
    ) -> AbstractContextManager[None]:
        selected_root = (
            _REPOSITORY_ROOT
            if repository_root is None
            else repository_root
        )
        return _guard_repository_state(selected_root)

    return create_guard


@pytest.fixture(scope="function")
def protected_repository_state(
    repository_write_guard: RepositoryWriteGuardFactory,
) -> Iterator[None]:
    """Guard real protected trees for a test that explicitly opts in."""

    with repository_write_guard():
        yield


@pytest.fixture(scope="session", autouse=True)
def fortress_protected_state_session_guard() -> Iterator[None]:
    """Detect protected-tree mutation across the configured session.

    FORTRESS-02I broadens the opt-in FORTRESS-02C guard so no configured
    certification test can silently mutate ``data/``, ``config/``,
    ``logs/``, or ``exports/``.

    The guard only reads. It never resets, restores, or repairs a file, it
    tolerates an already-dirty working tree because it compares before
    against after rather than against Git, and it reports the affected
    relative paths. Session teardown runs after every function-scoped
    fixture, so a late write is still detected.
    """

    before = _snapshot_protected_state(_REPOSITORY_ROOT)

    yield

    after = _snapshot_protected_state(_REPOSITORY_ROOT)
    changes = _protected_state_changes(before, after)

    if changes:
        details = "\n".join(f"- {change}" for change in changes)
        raise AssertionError(
            "protected repository runtime state changed during the "
            "configured session:\n" + details
        )
